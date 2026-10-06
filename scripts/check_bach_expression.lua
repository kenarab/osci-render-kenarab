-- Verifica el entregable controlable y exporta cuatro timbres aislados comparables.
-- luajit scripts/check_bach_expression.lua [WAV, por defecto recordings/005-voces.wav]
local ffi=require("ffi")
assert(ffi.abi("le"))
local f=assert(io.open("experiments/005-aire-de-bach/aire-control.lua")); local code=f:read("*a"); f:close()
local function load(rate)
    local e=setmetatable({step=0,sample_rate=rate,slider_a=.375,slider_b=.65,slider_c=.45,slider_d=.7,slider_e=.2},{__index=_G})
    return setfenv(assert(loadstring(code)),e),e
end
local function check(p)
    for _,v in ipairs(p) do assert(v==v and math.abs(v)<1) end
end
for _,rate in ipairs({44100,48000}) do
    local play,e=load(rate)
    local p=play(); assert(e.bach_air.base_bpm==32)
    local previous=p; local delta=0
    for i=1,rate*9 do
        e.step=i
        local value=i<rate*3 and 0 or (i<rate*6 and 1 or .5)
        e.slider_a,e.slider_b,e.slider_c,e.slider_d,e.slider_e=value,value,value,value,value
        local beat=e.bach_air.beat
        p=play(); check(p)
        assert(e.bach_air.beat>beat)
        for j=1,3 do delta=math.max(delta,math.abs(p[j]-previous[j])) end
        previous=p
        if i==rate*3-1 then assert(math.abs(e.bach_air.base_bpm-20)<1e-8) end
        if i==rate*6-1 then assert(math.abs(e.bach_air.base_bpm-52)<1e-8) end
        if i%257==0 then
            for _,v in ipairs(e.bach_air.voices) do
                if v.radius then
                    local x,y,z,r=v.gx,v.gy,v.gz,v.radius
                    assert(math.abs((x*x+y*y+z*z+.78^2-r*r)^2-4*.78^2*(x*x+y*y))<1e-11)
                end
            end
        end
    end
    assert(delta<.25)
    local s=e.bach_air; local a=s.a
    e.slider_a=0/0; e.slider_b=math.huge; e.step=e.step+1; check(play()); assert(s.a==a)
    print(string.format("Controles 20/52 BPM, expresión, polinomios, inválidos y continuidad: %d Hz; delta %.5f",rate,delta))
end

local count=48000*6
local pcm=ffi.new("int16_t[?]",count*2*4)
local signatures={}
for voice=1,4 do
    local play,e=load(48000); play()
    -- Misma nota C4 y duración para comparar el perfil, sin diferencias de partitura.
    local s=e.bach_air
    s.notes={{{0,8,60}},{{0,8,60}},{{0,8,60}},{{0,8,60}}}
    for j=1,4 do s.weights[j]=j==voice and 1 or 0; s.voices[j].index=1 end
    local values=ffi.new("double[?]",count*2); local energy=0
    for i=0,count-1 do
        e.step=i+1; local p=play()
        local t=math.max(0,math.min(1,(6-i/48000)/.35)); local fade=t*t*(3-2*t)
        for a=1,2 do values[2*i+a-1]=p[a]*fade; energy=energy+(p[a]*fade)^2 end
    end
    local rms=math.sqrt(energy/(count*2)); assert(rms>.05)
    local gain=.13/rms; local peak=0
    for i=0,count*2-1 do
        local v=values[i]*gain; peak=math.max(peak,math.abs(v)); assert(math.abs(v)<.95)
        pcm[(voice-1)*count*2+i]=math.floor(v*32767+.5)
    end
    signatures[voice]=rms
    print(string.format("Voz %d: N=%d r_base=%.2f filtro=%.1f·f; escucha RMS 0.13, pico %.4f",voice,s.turns[voice],s.radii[voice],s.cutoff[voice],peak))
end
assert(math.abs(signatures[1]-signatures[2])>1e-4 and math.abs(signatures[2]-signatures[3])>1e-4)
local function uint(n,bytes)
    local out=""; for _=1,bytes do out=out..string.char(n%256); n=math.floor(n/256) end; return out
end
local size=count*4*4
f=assert(io.open(arg[1] or "recordings/005-voces.wav","wb"))
f:write("RIFF",uint(36+size,4),"WAVEfmt ",uint(16,4),uint(1,2),uint(2,2),uint(48000,4),
    uint(192000,4),uint(4,2),uint(16,2),"data",uint(size,4),ffi.string(pcm,size)); f:close()
print("OK: cuatro timbres, seis segundos cada uno; aceptación por escucha pendiente.")
