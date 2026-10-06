-- luajit scripts/render_bach_air.lua [prefijo de salida, por defecto recordings/005-aire]
-- Segundo argumento opcional: ruta del Lua (p. ej. aire-adagio.lua).
-- Ejecuta el mismo Lua entregable y valida la señal mientras escribe PCM estéreo.
local ffi=require("ffi")
assert(ffi.abi("le"))
local prefix=arg[1] or "recordings/005-aire"
local source=assert(io.open(arg[2] or "experiments/005-aire-de-bach/aire.lua")):read("*a")
local engine=setfenv(assert(loadstring(source)),_G)
local function uint(n,bytes)
    local out=""
    for _=1,bytes do out=out..string.char(n%256); n=math.floor(n/256) end
    return out
end
local wav=assert(io.open(prefix..".wav","wb"))
wav:write(string.rep("\0",44))
sample_rate=48000
step=0
slider_a,slider_b,slider_c,slider_d,slider_e=0,0,0,0,0
local pcm=ffi.new("int16_t[?]",96000)
local frames,used,peak,energy,maxdelta=0,0,0,0,0
local previous={0,0,0}
local transitions={0}
local boundaries={24,48,96,144}
local nextboundary=1
while frames<sample_rate*600 do
    step=frames
    local p=engine()
    for axis=1,3 do
        local v=p[axis]
        assert(v==v and math.abs(v)<1,"señal no finita o fuera de rango")
        peak=math.max(peak,math.abs(v))
        maxdelta=math.max(maxdelta,math.abs(v-previous[axis]))
    end
    energy=energy+p[1]^2+p[2]^2
    previous=p
    pcm[used*2]=math.floor(p[1]*32767+0.5)
    pcm[used*2+1]=math.floor(p[2]*32767+0.5)
    used=used+1; frames=frames+1
    if used==48000 then wav:write(ffi.string(pcm,used*4)); used=0 end
    if boundaries[nextboundary] and bach_air.beat>=boundaries[nextboundary] then
        transitions[#transitions+1]=frames/sample_rate
        print(string.format("Sección %d: %.2f s",nextboundary,frames/sample_rate))
        nextboundary=nextboundary+1
    end
    if bach_air.done then break end
end
assert(bach_air.done and #transitions==5,"obra incompleta")
assert(previous[1]==0 and previous[2]==0 and previous[3]==0)
if source:find('interpretation="adagio"',1,true) then
    assert(frames/sample_rate > 230.046*1.3, "adagio insuficientemente lento")
end
assert(energy>100 and peak>0.1 and maxdelta<0.25,"actividad/continuidad inesperada")
wav:write(ffi.string(pcm,used*4))
wav:seek("set",0)
wav:write("RIFF",uint(36+frames*4,4),"WAVEfmt ",uint(16,4),uint(1,2),uint(2,2),
    uint(48000,4),uint(192000,4),uint(4,2),uint(16,2),"data",uint(frames*4,4))
wav:close()
local report=assert(io.open(prefix..".json","w"))
report:write(string.format('{"duration":%.9f,"frames":%d,"sample_rate":48000,"peak":%.9f,"rms_xy":%.9f,"max_delta":%.9f,"sections":[%s]}\n',
    frames/48000,frames,peak,math.sqrt(energy/(2*frames)),maxdelta,table.concat(transitions,",")))
report:close()
-- Reinicio TAKE sin depender de que el editor borre sus variables.
local take=assert(tonumber(source:match("local TAKE = (%d+)")))
local restart=assert(loadstring((source:gsub("local TAKE = "..take,"local TAKE = "..(take+1),1))))
local p=restart()
assert(bach_air.take==take+1 and p[1]==0 and p[2]==0)
-- Movimientos bruscos de perillas a 44.1 kHz: cota y reloj monotónico.
local controls=assert(loadstring((source:gsub("local USAR_SLIDERS = false","local USAR_SLIDERS = true",1))))
sample_rate=44100
for i=0,44100*8 do
    step=i
    local target=i<44100*2 and 0 or (i<44100*5 and 1 or 0)
    slider_a,slider_b,slider_c,slider_d,slider_e=target,target,target,target,target
    local oldbeat=bach_air.rate==sample_rate and bach_air.beat or 0
    p=controls()
    assert(bach_air.beat>=oldbeat or i==0)
    for _,v in ipairs(p) do assert(v==v and math.abs(v)<1) end
end
print(string.format("OK: %.2f s; pico %.5f; RMS %.5f; delta máximo %.5f; TAKE y CC aprobados",frames/48000,peak,math.sqrt(energy/(2*frames)),maxdelta))
