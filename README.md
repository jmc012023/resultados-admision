# RESULTADOS DE ADMISION UNT DESDE 2019-I HASTA 2024-II

# OBJETIVO

Extraer y transformar todos los resultados de admision a la UNT desde 2019-I hasta 2024-II de la pagina web `https://www.admisionunt.info/padron`

# DETALLES

El script main.py genera un archivo csv llamado unt_results.csv, que contiene toda la data transformada. El proyecto por el momento no pretende automatizar, ya que agregar nueva data se requiere un nuevo analisis de la data y verificar si la estructura de la nueva data no genera conflicto con la ya generada, ya que la estructura de la data en la mayoria de los casos ha ido cambiando a traves del tiempo

# INICIAR EL PROYECTO

Tener instalado Python3.10 o versiones superiores y pip, y ejecutar `pip install -r requirements.txt`. Ejecutar el script main.py con `python3 main.py`. Este script genera dos archivos csv, uno la ruta `/get/data/raw_data.csv` y otro en `/unt_results.csv`. Actualmente estos archivos ya se encuentran en el proyecto por motivos didacticos, pero se los puede borrar antes de ejecutar el script main.py, y el script los creara nuevamente

# RESULTADOS

- Se extrajeron 135 179 filas de la pagina web y estos se transformaron a 115 385 filas. Los datos transformados se encuentra en la ruta `/unt_results.csv`

# CONSIDERACIONES

- Los archivos `*.ipynb` sirven de documentacion para mostrar el como los datos se fueron transformando, pero el scrip main.py no utiliza estos archivo, ya que todo el codigo se divido en modulos

- El campo area no va ser considerado en esta version ya que a lo largo del tiempo las carreras que pertenecian a determinada area ahora ya no forman parte de esa area y forman parte de otra area

- Los resultados para los examenes extraordinarios 2024 II en la pagina web en algunos resultados solo se indica el lugar, debido a ello se asumio que la modalidad fue excelencia

- Algunos examenes extraordinarios, en la pagina web, no se especificaban el lugar en donde se realizaron. El lugar se indicaban dentro de los enlaces, los cuales para estos casos todos fueron trujillo

- No se utilizan tildes para evitar conflictos entre los sistemas operativos y el sistema de control de versiones (git)
