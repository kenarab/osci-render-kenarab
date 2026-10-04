-- Ejecutar desde la raíz. Solo biblioteca estándar de Lua/LuaJIT.
local root = "experiments/001-primeras-curvas/"
local files = {"01-circle.lua", "02-lissajous.lua", "03-torus-path.lua"}
for _, name in ipairs(files) do
    local curve = assert(loadfile(root .. name))
    local first
    for i = 0, 4096 do
        phase = 2 * math.pi * i / 4096
        local point = curve()
        assert(type(point) == "table" and #point == 3, name .. ": formato")
        for _, value in ipairs(point) do
            assert(type(value) == "number" and value == value and math.abs(value) <= 0.5,
                name .. ": coordenada no finita o fuera de amplitud")
        end
        local x, y, z = point[1], point[2], point[3]
        if name == "01-circle.lua" then
            assert(math.abs(x*x + y*y - 0.16) < 1e-12, "radio del círculo")
        elseif name == "03-torus-path.lua" then
            local R, r = 0.35, 0.12
            local residual = (x*x+y*y+z*z+R*R-r*r)^2 - 4*R*R*(x*x+y*y)
            assert(math.abs(residual) < 1e-12, "punto fuera del toro")
        end
        if i == 0 then
            first = point
        elseif i == 4096 then
            for axis = 1, 3 do
                assert(math.abs(point[axis] - first[axis]) < 1e-12, name .. ": curva abierta")
            end
        end
    end
    print("OK " .. name .. ": 4097 muestras, amplitud y cierre")
end
