-- Lua 5.1+/LuaJIT; ejecutar desde la raíz. WAV opcional como primer argumento.
local path = "experiments/002-estudio-de-un-toro/estudio.lua"
local file = assert(io.open(path, "r"))
local source = file:read("*a")
file:close()
local compile = loadstring or load
local function uint(value, bytes)
    local out = ""
    for _ = 1, bytes do
        out = out .. string.char(value%256)
        value = math.floor(value/256)
    end
    return out
end
local output
if arg[1] then
    output = assert(io.open(arg[1], "wb"))
    local size = 80*48000*4
    output:write("RIFF", uint(36+size,4), "WAVEfmt ", uint(16,4),
        uint(1,2), uint(2,2), uint(48000,4), uint(192000,4),
        uint(4,2), uint(16,2), "data", uint(size,4))
end
for _, rate in ipairs({44100, 48000}) do
    sample_rate, step, torus_study = rate, 0, nil
    local curve = assert(compile(source))
    local previous, peak, energy = nil, 0, {0,0,0}
    local probes, buffer = {}, {}
    for i = 0, 80*rate do
        step = i
        local point = curve()
        assert(#point == 3, "se esperan tres coordenadas")
        local section = i < 20*rate and 1 or (i < 60*rate and 2 or 3)
        for axis = 1, 3 do
            local v = point[axis]
            assert(v == v and math.abs(v) <= 0.424, "señal no finita o fuera de cota")
            peak = math.max(peak, math.abs(v))
            energy[section] = energy[section] + v*v
            -- Un cambio de nota debe pasar cerca del cero, no saltar de objeto.
            local beat = i/rate*96/60
            if previous and math.abs(beat*2-math.floor(beat*2+0.5)) < 4/rate then
                assert(math.abs(v-previous[axis]) < 0.001, "salto en cambio de nota")
            end
        end
        if i%rate == 0 then probes[#probes+1] = point end
        if output and rate == 48000 and i < 80*rate then
            for axis = 1, 2 do
                local pcm = math.floor(point[axis]*32767+0.5)
                buffer[#buffer+1] = uint(pcm%65536,2)
            end
            if #buffer >= 8192 then output:write(table.concat(buffer)); buffer = {} end
        end
        previous = point
    end
    assert(previous[1] == 0 and previous[2] == 0 and previous[3] == 0, "fin sin silencio")
    for _, value in ipairs(energy) do assert(value > 1, "sección sin actividad") end
    if output and rate == 48000 then output:write(table.concat(buffer)) end
    -- Repetición completa: comparar muestras de control sin cambiar la cadencia.
    torus_study = nil
    for i = 0, 80*rate do
        step = i
        local point = curve()
        if i%rate == 0 then
            for axis = 1, 3 do
                assert(point[axis] == probes[i/rate+1][axis], "resultado no determinista")
            end
        end
    end
    local restart = assert(compile((source:gsub("local TAKE = 1", "local TAKE = 2", 1))))
    step = 81*rate
    local first = restart()
    assert(torus_study.origin == step and torus_study.take == 2, "TAKE no reinicia")
    assert(first[1] == 0 and first[2] == 0 and first[3] == 0, "reinicio sin fade")
    print(string.format("OK %d Hz: 80 s, 3 secciones, pico %.6f, continuidad, determinismo, TAKE", rate, peak))
end
if output then output:close(); print("WAV: " .. arg[1]) end
