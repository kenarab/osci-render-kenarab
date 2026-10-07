-- REC-05: controles, reinicio y voces aisladas de superficies récord.
-- Validacion de controles y ocho voces aisladas, mismo C4, RMS 0.13.
local ffi=require('ffi')
local function load(family,live,rate)
    local f=assert(io.open('experiments/009-bach-surfer-records/aire-'..family..(live and '-control' or '')..'.lua'))
    local code=f:read('*a');f:close()
    local env=setmetatable({sample_rate=rate,step=0,slider_a=.375,slider_b=.5,slider_c=0,slider_d=0,slider_e=0},{__index=_G})
    return setfenv(assert(loadstring(code)),env),env
end
local function uint(n,bytes)
    local out='';for _=1,bytes do out=out..string.char(n%256);n=math.floor(n/256) end;return out
end
for _,family in ipairs({'seda','cristal'}) do
    for _,rate in ipairs({44100,48000}) do
        local play,e=load(family,true,rate);local previous={0,0,0};local delta=0
        for i=0,rate*4 do
            e.step=i;e.slider_a=i<rate*2 and 0 or 1;e.slider_b=e.slider_a
            local old=e.bach_air and e.bach_air.beat or 0
            local p=play();assert(e.bach_air.beat>=old)
            for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<1);delta=math.max(delta,math.abs(p[a]-previous[a])) end
            previous=p
        end
        assert(delta<.25)
        e.step=0;local p=play();assert(p[1]==0 and p[2]==0)
        print(family,rate,'continuidad y reinicio OK',delta)
    end
    local count=48000*4
    local pcm=ffi.new('int16_t[?]',count*2*4)
    for voice=1,4 do
        local play,e=load(family,false,48000);play()
        local s=e.bach_air;s.notes={{{0,8,60}},{{0,8,60}},{{0,8,60}},{{0,8,60}}}
        for j=1,4 do s.weights[j]=j==voice and 1 or 0 end
        local values=ffi.new('double[?]',count*2);local energy=0
        for i=0,count-1 do
            e.step=i+1;local p=play();local t=math.max(0,math.min(1,(4-i/48000)/.3));local fade=t*t*(3-2*t)
            for a=1,2 do local v=p[a]*fade;values[i*2+a-1]=v;energy=energy+v*v end
        end
        local rms=math.sqrt(energy/(count*2));assert(rms>.01)
        for i=0,count*2-1 do
            local v=values[i]*.13/rms;assert(math.abs(v)<.95)
            pcm[(voice-1)*count*2+i]=math.floor(v*32767+.5)
        end
    end
    local size=count*4*4
    local f=assert(io.open('recordings/009-'..family..'-voces.wav','wb'))
    f:write('RIFF',uint(36+size,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(48000,4),uint(192000,4),uint(4,2),uint(16,2),'data',uint(size,4),ffi.string(pcm,size));f:close()
    print(family,'cuatro voces x 4s, RMS igualado 0.13')
end
