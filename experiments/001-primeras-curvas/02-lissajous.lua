-- Editar p/q con valores enteros mantiene el cierre por ciclo.
local p = 3
local q = 2
local amplitude = 0.4
local offset = math.pi / 2
return {
    amplitude * math.sin(p * phase + offset),
    amplitude * math.sin(q * phase),
    0
}
