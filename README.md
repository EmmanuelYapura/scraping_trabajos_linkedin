# Scraping para trabajos en LinkedIn

*Proyecto de automatizacion y scraping de ofertas laborales utilizando Selenium y BeautifulSoup en la pagina LinkedIn*

## Descripcion proyecto

*El proyecto inicia sesion de manera automatica en LinkedIn mediante credenciales guardadas en variables de entorno, 
luego navega hasta la seccion empleos para realizar una busqueda y extraer los datos obtenidos como por ejemplo: titulo de la publicacion.
Para finalizar estos datos extraidos los puedo ver mediante la consola o en un archivo JSON.*

## Tecnologias 

-[Python 3](https://www.python.org/)
-[Selenium](https://pypi.org/project/selenium/)
-[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
-[python-dev](https://pypi.org/project/python-dotenv/)

## Instalacion y uso

*Primero clonamos el repositorio*

``` 
git clone https://github.com/EmmanuelYapura/scraping_trabajos_linkedin "nombre a elección" 
```

*Creamos y activamos un entorno virtual*

```
python -m venv venv 
```

- Para Windows
``` 
venv/Scripts/activate
```
- Para Linux/macOs
``` 
source venv/bin/activate
```

*Instalamos las dependencias*

``` 
pip install -r requirements.txt
```

*Configuramos las variables de entorno*

``` 
crear un archivo .env
```
``` 
CORREO="ejemplo@ejemplo.com"
CONTRA="tu_contrasenia"
```

*Ejecutamos el script*

``` 
python main.py
```
