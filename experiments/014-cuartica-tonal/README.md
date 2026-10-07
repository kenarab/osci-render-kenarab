# Cuártica: tono y cobertura separados

EXP-050 / CUA-01…04. Ensayo independiente de Bach y Piazzolla.

[Comparación visual](../../recordings/014-cuartica-tonal.png) ·
[WAV de 6 segundos](../../recordings/014-cuartica-tonal.wav) ·
[Lua autónomo](cuartica.lua) · [Lua controlable](cuartica-control.lua).

Ecuación: `X^4+3Y^4+6Z^4+k*(X^2+Y^2+Z^2)=1`, k=.5 inicialmente.
El retorno es XYZ, con escala uniforme .42 y rotaciones 3D. No hay OBJ, filtro,
proyección previa ni notas MIDI. La plantilla reutilizable está en la biblioteca.

En el ejercicio anterior el giro longitudinal era 24 veces el barrido de 24 Hz
(576 Hz). Aquí elegimos 110 Hz longitudinal y 7 Hz latitudinal por separado.
Esto cambia el espectro, pero no demuestra que el sonido resulte agradable.
La cuártica es suave y convexa; no es una superficie récord con singularidades.

| Control | Función | Valor inicial |
| --- | --- | --- |
| A | Giro de escena, 0–.2 rad/s; cero pausa sin cortar sonido | .5 |
| B | Portadora longitudinal, 80–160 Hz | .375 → 110 Hz |
| C | Coeficiente k, .1–.9 | .5 → k=.5 |
| D | Cobertura latitudinal, 4–12 Hz | .375 → 7 Hz |

Poner controles del host en Static para pruebas manuales. El preset autónomo
ignora sliders y permite comparar sin LFO heredados. No se cargó automáticamente.

La imagen compara malla con caras, barrido XYZ real con cámara, y su XY.
La ventana de 143 ms enseña el recorrido, no un relleno simultáneo. El visor
interactivo [xyz-stage](../../apps/xyz-stage/index.html) permite seleccionar
cuartica y girar la referencia con caras; su recorrido superpuesto pertenece
al ejercicio 012, no al nuevo 014. Desactivar ese recorrido para comparar formas.
La referencia estática usa k=.5: no sigue cambios de C en el host.

Verificado a 16/44.1/48 kHz: residuo de F=0 <2.7e-15 tras invertir giro/escala,
pico <.400, energía en tres ejes y 128/128 celdas angulares visitadas en un segundo.
Esto comprueba cobertura discreta, no cobertura continua ni fidelidad de un
renderizador. Pausa de escena, controles y reinicio aprobados. Sin limitación
espectral: aliasing posible. Escucha, tamaño visual en Pro y calidad artística
pendientes. El WAV conserva XY y no se normaliza.

Reproducir sin activar audio:

```sh
python3 scripts/build_tonal_surface.py
luajit scripts/check_tonal_surface.lua
python3 scripts/preview_tonal_surface.py
```

El render usa Pillow ya disponible. Las grabaciones, CSV XYZ e imagen generada
quedan en recordings, fuera de Git. Validación numérica en validacion.json.
