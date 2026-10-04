-- Curva continua sobre un toro algebraico; no dibuja toda la superficie.
-- (x*x+y*y+z*z+R*R-r*r)^2 - 4*R*R*(x*x+y*y) = 0
local R = 0.35
local r = 0.12
local u = 2 * phase
local v = 3 * phase
return {
    (R + r * math.cos(v)) * math.cos(u),
    (R + r * math.cos(v)) * math.sin(u),
    r * math.sin(v)
}
