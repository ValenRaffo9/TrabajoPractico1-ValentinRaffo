import requests
from bs4 import BeautifulSoup
import csv

# Indicamos la ruta de la web que deseamos acceder
url_page = 'https://billboard.com/charts/hot-100/'

# Hacer el request a esa ruta y procesamos el HTML mediante un objeto de tipo BeautifulSoup
page = requests.get(url_page).text 
soup = BeautifulSoup(page, features="html.parser")

# Obtenemos los títulos de las canciones
# Los títulos se encuentran en elementos <h3> con la clase "a-no-trucate"
titulos = soup.findAll('h3', class_='a-no-trucate')

# Crear el archivo para guardar los datos
with open('canciones_billboard.csv', 'w', newline='', encoding='utf-8') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['Título'])  # Escribir el encabezado en el CSV

    for titulo in titulos:
        nombre_cancion = titulo.get_text(strip=True)  # Obtener el texto sin espacios
        writer.writerow([nombre_cancion])  # Escribir el nombre de la canción en el CSV
        print(f'Canción guardada: {nombre_cancion}')  # Imprimir el nombre de la canción guardada

print("Los títulos de las canciones han sido guardados en 'canciones_billboard.csv'.")
 