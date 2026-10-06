-- LuaJIT: verifica partituras completas y opcionalmente exporta WAV estéreo.
-- luajit scripts/check_live_studies.lua [directorio-de-salida-existente]
local ffi = require("ffi")
assert(ffi.abi("le"), "exportador WAV requiere little-endian")
local studies = {{"003-orbitas",60}, {"004-cristal",128*60/108}}
local function uint(n,bytes)
    local out=""
    for _=1,bytes do out=out..string.char(n%256); n=math.floor(n/256) end
    return out
end
local function load_score(path)
    local f=assert(io.open(path)); local code=f:read("*a"); f:close()
    local env=setmetatable({step=0,sample_rate=48000}, {__index=_G})
    -- Comprobar el polinomio sobre las coordenadas reales antes de cámara.
    code=code:gsub("local tilt=", "assert(math.abs((x/aa)^POWER+(y/bb)^POWER+(z/cc)^POWER-1)<1e-10); local tilt=",1)
    return setfenv(assert(loadstring(code)),env),env,code
end
local function check(point)
    assert(#point==3)
    for _,v in ipairs(point) do assert(v==v and math.abs(v)<0.8,"señal inválida") end
end
for _,item in ipairs(studies) do
    local name,duration=item[1],item[2]
    local score,env,code=load_score("experiments/"..name.."/estudio.lua")
    local count=math.ceil(duration*48000)+2
    local pcm=arg[1] and ffi.new("int16_t[?]",count*2) or nil
    local energy={0,0,0}; local peak=0; local probes={}
    for i=0,count-1 do
        env.step=i
        local p=score(); check(p)
        local section=math.min(3,math.floor(i/count*3)+1)
        for axis=1,3 do
            peak=math.max(peak,math.abs(p[axis]))
            energy[section]=energy[section]+p[axis]^2
        end
        if i<4096 then probes[i+1]=p end
        if pcm then
            pcm[i*2]=math.floor(p[1]*32767+0.5)
            pcm[i*2+1]=math.floor(p[2]*32767+0.5)
        end
    end
    assert(env.algebra_score.done,"la pieza no terminó")
    for _,v in ipairs(energy) do assert(v>1,"sección sin actividad") end
    local p=score(); assert(p[1]==0 and p[2]==0 and p[3]==0)
    -- Reinicio al retroceder el contador y reproducción determinista.
    for i=0,4095 do
        env.step=i; p=score()
        for axis=1,3 do assert(p[axis]==probes[i+1][axis]) end
    end
    local restart=setfenv(assert(loadstring((code:gsub("local TAKE = 1","local TAKE = 2",1)))),env)
    env.step=5000; restart(); assert(env.algebra_score.take==2)
    -- Barridos extremos y valores fuera de rango, con cambio de sample rate.
    for _,rate in ipairs({44100,48000}) do
        env.sample_rate=rate
        for i=0,rate*4 do
            env.step=i
            local target=i<rate and -1 or (i<rate*2 and 2 or 0.5)
            env.slider_a=target; env.slider_b=target; env.slider_c=target
            env.slider_d=target; env.slider_e=target
            check(score())
        end
        local s=env.algebra_score
        assert(math.abs(s.a-0.5)<1e-5 and math.abs(s.e-0.5)<1e-5)
    end
    if pcm then
        local f=assert(io.open(arg[1].."/"..name..".wav","wb"))
        local size=count*4
        f:write("RIFF",uint(36+size,4),"WAVEfmt ",uint(16,4),uint(1,2),uint(2,2),
            uint(48000,4),uint(192000,4),uint(4,2),uint(16,2),"data",uint(size,4),ffi.string(pcm,size))
        f:close()
    end
    print(string.format("OK %s: %.3f s, pico %.4f, polinomio, fin, reinicio, controles y determinismo",name,duration,peak))
end
