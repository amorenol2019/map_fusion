# Fusión de mapas 

This repo contains information about map_fusion in 2D. Part of my bachelor thesis.

Para realizar el mapping fusion de los mapas que generan dos robots por separado, lo que buscamos son métodos para fusionar dos imágenes en una nueva.

## Estado del arte
- [ ] Los algoritmos no deberían descartar la información contenida en las imágenes de partida.
- [ ] No deberían introducir inconsistencias que pudieran **inducir a error**.
- [ ] Deben ser realizables, robustos y deben capacidad de tolerar imperfecciones.

## Fusión de imágenes con media
Una primera aproximación son los diferentes algoritmos de media[^1].
- Basados en la **combinación de los coeficientes**
  - Media *aritmética*
  - Media ponderada *gaussiana*
  - Media ponderada *laplaciana*
- Basados en la **selección de coeficientes**
  - *Varianza* sobre una ventana de coeficientes
  - Medición del *nivel de actividad* basado en coeficientes

### Combinación de coeficientes
Consiste en combinar coeficientes aplicando la media entre las dos imágenes. Esto deriva a una nueva imagen que contiene las características de ambas pero cuyos detalles podrían no estar del todo definidos.
Los algoritmos se pueden aplicar en dos dominios diferentes:
- **Dominio espacial.**

  Método de media aritmética es el único que usa este dominio.
  
- **Dominio Wavelet.**

  Las imágenes originales se descomponen a través de la transformada de wavelet. Esta transformada nos devuelve cuatro matrices por cada imagen: una de aproximación y tres de detalles (vertical, horizontal y diagonal). Se hace la media aritmética de ambas aproximaciones y para los detalles dependerá de cada algoritmo aplicado.
![image](https://user-images.githubusercontent.com/79024752/224028186-2116f094-5e3e-4e0f-8dc4-dafab4329f52.png)

### Selección de coeficientes
Se pueden aplicar a toda la imagen o a subventanas de coeficientes. Consiste en elegir el mejor pixel según el método aplicado.

Para este método, seguiremos los mismos pasos usados para los algoritmos calculados sobre el dominio wavelet.

Estos algoritmos sólo se pueden usar sobre imágenes que sean iguales y simplemente tenga diferencias en los detalles visuales (cambio de valores en los píxeles). En cambio, para fusionar dos mapas que nos provienen de dos robots diferentes, necesitamos un algoritmo que los fusione independientemente de la orientación, las condiciones de luz, perspectiva, etc. Este nuevo algoritmo tendria que encontrar las coincidencias en ambas imágenes y unirlas en una nueva. Para ello, podríamos hacer uso de descriptores.

## Fusión de imágenes usando descriptores




## Referencias
[^1]:https://repositorio.upct.es/bitstream/handle/10317/3429/pfc5406.pdf%3Bjses
[^2]:https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
