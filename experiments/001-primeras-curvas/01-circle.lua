-- osci-render: phase recorre [0, 2*pi). Radio conservador para la prueba.
local radius = 0.4
return {radius * math.cos(phase), radius * math.sin(phase), 0}
