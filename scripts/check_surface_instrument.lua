-- luajit scripts/check_surface_instrument.lua [salida existente: recordings]
-- Prueba los Lua entregables; PCM sin efectos del host. No requiere Lua externo en el host.
local ffi=require("ffi")
assert(ffi.abi("le"))
local root="experiments/007-toro-sonoro/"
local output=arg[1] or "recordings"
local function load(name,sliders,rate)
    local f=assert(io.open(root..name..".lua")); local code=f:read("*a"); f:close()
    if sliders then code=code:gsub("local USAR_SLIDERS = false","local USAR_SLIDERS = true",1) end
    local env=setmetatable({sample_rate=rate or 48000,step=0}, {__index=_G})
    return setfenv(assert(loadstring(code)),env),env,code
end
local function uint(n,bytes)
    local out=""
    for _=1,bytes do out=out..string.char(n%256); n=math.floor(n/256) end
    return out
end
local function wav(path,pcm,count)
    local f=assert(io.open(path,"wb")); local size=count*4
    f:write("RIFF",uint(36+size,4),"WAVEfmt ",uint(16,4),uint(1,2),uint(2,2),
        uint(48000,4),uint(192000,4),uint(4,2),uint(16,2),"data",uint(size,4),ffi.string(pcm,size))
    f:close()
end
local function finite(p)
    for _,v in ipairs(p) do assert(v==v and math.abs(v)<0.95,"señal inválida o clipping") end
end
local reports={}
for _,name in ipairs({"suave","cuerpo","aire"}) do
    local play,e=load(name,false)
    local count=48000*12
    local pcm,raw=ffi.new("int16_t[?]",count*2),ffi.new("int16_t[?]",count*2)
    local peak,energy,delta,sumx,sumy=0,0,0,0,0
    local px,py=0,0
    local frames={}
    for i=0,count-1 do
        e.step=i
        local p=play(); finite(p)
        local s=e.surface_voice
        if i%257==0 then
            local x,y,z=s.gx,s.gy,s.gz
            assert(math.abs((x*x+y*y+z*z+0.62^2-s.radius^2)^2-4*0.62^2*(x*x+y*y))<1e-12)
        end
        -- Cierre editorial del clip de prueba; instrumento vivo de duración libre.
        local t=math.max(0,math.min(1,(12-i/48000)/0.4))
        local fade=t*t*(3-2*t)
        local x,y=p[1]*fade,p[2]*fade
        peak=math.max(peak,math.abs(x),math.abs(y))
        energy=energy+x*x+y*y; sumx=sumx+x; sumy=sumy+y
        delta=math.max(delta,math.abs(x-px),math.abs(y-py)); px,py=x,y
        pcm[i*2]=math.floor(x*32767+0.5); pcm[i*2+1]=math.floor(y*32767+0.5)
        raw[i*2]=math.floor(s.rawx*fade*32767+0.5); raw[i*2+1]=math.floor(s.rawy*fade*32767+0.5)
        if i%1600==0 then
            frames[#frames+1]=string.format('{"spin":%.10f,"r":%.10f,"effective_r":%.10f}',s.spin,s.radius,s.effective_radius)
        end
    end
    local rms=math.sqrt(energy/(count*2))
    assert(rms>0.05 and delta<0.04)
    assert(math.abs(sumx/count)<0.001 and math.abs(sumy/count)<0.001)
    wav(output.."/007-"..name..".wav",pcm,count)
    wav(output.."/007-"..name.."-raw.wav",raw,count)
    local report=string.format('{"voice":"%s","duration":12,"sample_rate":48000,"peak":%.9f,"rms":%.9f,"max_delta":%.9f,"dc":[%.9f,%.9f],"frames":[%s]}',
        name,peak,rms,delta,sumx/count,sumy/count,table.concat(frames,","))
    local f=assert(io.open(output.."/007-"..name..".json","w")); f:write(report,"\n"); f:close()
    reports[#reports+1]=rms
    print(string.format("%s: pico %.5f RMS %.5f delta %.5f; toro y DC aprobados",name,peak,rms,delta))
end
local spread=20*math.log(math.max(unpack(reports))/math.min(unpack(reports)))/math.log(10)
assert(spread<1,"comparación de volumen desigual")

for _,rate in ipairs({44100,48000}) do
    local play,e,code=load("aire",true,rate)
    e.slider_a,e.slider_b,e.slider_c,e.slider_d,e.slider_e=0,0.5,0.5,0.55,0.35
    play()
    -- A=0: tras suavizado, diez segundos con cámara detenida y audio activo.
    for i=1,rate*2 do e.step=i; play() end
    local spin=e.surface_voice.spin
    local energy=0
    for i=rate*2+1,rate*12 do
        e.step=i; local p=play(); finite(p); energy=energy+p[1]^2+p[2]^2
    end
    assert(math.abs(e.surface_voice.spin-spin)<1e-12 and energy>10)
    -- B no mueve la escena; cambios extremos, silencio E=0 y datos inválidos.
    local previous={0,0,0}; local maxdelta=0
    for i=1,rate*3 do
        e.step=e.step+1
        e.slider_b=i<rate and 1 or 0
        e.slider_c=i<rate and -1 or 2
        e.slider_d=i<rate and 1 or 0
        e.slider_e=i<rate*2 and 1 or 0
        local p=play(); finite(p)
        if i>1 then for a=1,2 do maxdelta=math.max(maxdelta,math.abs(p[a]-previous[a])) end end
        previous=p
    end
    assert(maxdelta<0.16 and math.abs(e.surface_voice.spin-spin)<1e-12)
    assert(math.abs(previous[1])+math.abs(previous[2])<1e-5)
    local old=e.surface_voice.radius
    e.slider_c=0/0; e.slider_a=math.huge; e.step=e.step+1; finite(play())
    assert(e.surface_voice.radius==old)
    local restart=setfenv(assert(loadstring((code:gsub("local TAKE = 1","local TAKE = 2",1)))),e)
    restart(); assert(e.surface_voice.take==2 and e.surface_voice.seconds==1/rate)
    e.step=0; restart(); assert(e.surface_voice.seconds==1/rate)
    print("Controles, pausa 10 s, independencia, inválidos, silencio y TAKE: "..rate)
end

-- Espectro real del Lua con controles estáticos: solo 1,23,24,25.
-- En los extremos 20/120 Hz son <=3000 Hz, por debajo de Nyquist a ambas tasas.
-- Proyectar sobre esos armónicos deja residuo casi cero; no basta medir clipping.
for _,rate in ipairs({44100,48000}) do
    for _,b in ipairs({0,1}) do
        local hz=20*6^b
        local cycles=(rate==44100 and b==1) and 2 or 1
        local n=math.floor(rate/hz*cycles+0.5)
        local play,e=load("cuerpo",true,rate)
        e.slider_a,e.slider_b,e.slider_c,e.slider_d,e.slider_e=0,b,1,0,0.35
        play(); local s=e.surface_voice
        s.a,s.b,s.c,s.d,s.e=0,b,1,0,0.35
        s.phase,s.spin,s.seconds=0,0,1
        local data={{},{}}; local energy=0
        for i=0,n-1 do
            e.step=i+1; local p=play()
            for a=1,2 do data[a][i+1]=p[a]; energy=energy+p[a]^2 end
        end
        local residual=0
        for a=1,2 do
            local recon={}; for i=1,n do recon[i]=0 end
            for _,h in ipairs({1,23,24,25}) do
                local c,t=0,0
                for i=0,n-1 do
                    local angle=2*math.pi*h*cycles*i/n
                    c=c+data[a][i+1]*math.cos(angle)*2/n
                    t=t+data[a][i+1]*math.sin(angle)*2/n
                end
                for i=0,n-1 do
                    local angle=2*math.pi*h*cycles*i/n
                    recon[i+1]=recon[i+1]+c*math.cos(angle)+t*math.sin(angle)
                end
            end
            for i=1,n do residual=residual+(data[a][i]-recon[i])^2 end
        end
        assert(residual/energy<1e-16,"energía inesperada fuera de los armónicos previstos")
        print(string.format("Espectro %d Hz / barrido %d Hz: residuo relativo %.3g",rate,hz,residual/energy))
    end
end
print(string.format("OK SUP-A03/A04/A05, TIM-A01/A02 y espectro estático A03; diferencia RMS %.3f dB. Host y escucha pendientes.",spread))
