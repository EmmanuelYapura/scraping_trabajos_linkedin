from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import json

load_dotenv()

class Empleo:
    def __init__(self, titulo: str, empresa: str , zona: str, link: str):
        self.titulo = titulo 
        self.empresa = empresa
        self.zona = zona
        self.link = link

    def mostrar_empleo(self):
        """ Muestra los detalles del empleo """
        print (f"{self.titulo} en {self.empresa}, {self.zona} - {self.link}")

class Usuario:
    def __init__(self, nombre: str, correo :str, contra: str):
        self.nombre = nombre
        self.correo = correo
        self.contra = contra
        self.lista_empleos = []

class UserInteraccion:
    def __init__(self, usuario: Usuario, driver: webdriver):
        self.usuario = usuario
        self.driver = driver

    def _ingresar_datos_usuario(self):
        """ Autocompleta los inputs con las credenciales del usuario 
        
        Parametros: 
        driver(webdriver): objeto webdriver para controlar el navegador web
        """
        self.driver.find_element(By.ID, "username").send_keys(self.usuario.correo)
        self.driver.find_element(By.ID, "password").send_keys(self.usuario.contra)

    def _marcar_checkbox(self):
        """ Marca el input-checkbox de recordar cuenta 
        
        Parametros: 
        driver(webdriver): objeto webdriver para controlar el navegador web
        """
        checkbox = self.driver.find_element(By.ID, "rememberMeOptIn-checkbox")
        self.driver.execute_script("arguments[0].click();", checkbox)

    def iniciar_session(self):
        """ Inicia sesion en linkedin, enviando los datos ingresados automaticamente
        
        Parametros: 
        driver(webdriver): objeto webdriver para controlar el navegador web
        """
        self._ingresar_datos_usuario()
        self._marcar_checkbox()
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

    def buscar_empleos(self, trabajos: str):
        """ Navega hasta la seccion de empleos para realizar una busqueda mediante una cadena enviada como parametro 
    
            Parametros: 
            driver(webdriver): objeto webdriver para controlar el navegador web
            trabajos(str): cadena de texto a ingresar en el buscador de empleos
        """
        btn_empleos = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="https://www.linkedin.com/jobs/"]'))
        )
        btn_empleos.click()

        input_empleos = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-label="Busca por cargo, aptitud o empresa"]'))
        )
        
        input_empleos.send_keys(trabajos)
        input_empleos.send_keys(Keys.RETURN)

    def obtener_lista_trabajos(self, divs_trabajos : list[BeautifulSoup]):
        """ Crea una lista de empleos
        
        Parametros: 
        driver(webdriver): objeto webdriver para controlar el navegador web
        divs_trabajos(lista de objetos BeautifuSoup): una lista con todos los elementos html (divs) para scrapear
        
        Retorna:
        list[Empleo]: retorna una lista de objetos Empleo
        """
        self.usuario.lista_empleos = [Empleo(
            titulo=div.find('strong').text,
            empresa=div.find_all('span', {'dir': 'ltr'})[0].text.strip(),
            zona=div.find_all('span', {'dir': 'ltr'})[1].text.strip(),
            link=div.find('a').get('href')
        ) for div in divs_trabajos]

    def cerrar_session(self):
        """ Cerrar sesion en linkedin """
        self.driver.find_element(By.CSS_SELECTOR, "div.global-nav__me").click()

        btn_cerrar_sesion = WebDriverWait(self.driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Cerrar sesión"))
        )
        btn_cerrar_sesion.click()

    def mostrar_empleos(self):
        """ Muestra los detalles de todos los empleos"""
        for empleo in self.usuario.lista_empleos:
            empleo.mostrar_empleo()

    def exportar_datos_json(self, nombre_archivo : str = "empleos.json"):
        """ Crea un archivo con los datos de la busqueda de empleo
         
        Parametros:
        nombre_archivo(str: opcional): sera el nombre del archivo con los empleos        
        """
        #Podria implementar una carpeta con funcionalidades y agregar esto a una funcion "convertir_a_diccionario"
        empleos_dict = [
            {
            "titulo": empleo.titulo,
            "empresa": empleo.empresa,
            "zona": empleo.zona,
            "link": empleo.link
            } 
            for empleo in self.usuario.lista_empleos
        ]

        with open (nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(empleos_dict,f,ensure_ascii=False,indent=4)

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")

usuario = Usuario('emmanuel', os.getenv("CORREO"), os.getenv("CONTRA"))
sesion = UserInteraccion(usuario, driver)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "username"))
)

sesion.iniciar_session()

sesion.buscar_empleos("python")

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-card-container"))
)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

contenedores = soup.find_all('div', class_='job-card-container')
sesion.obtener_lista_trabajos(contenedores)

sesion.mostrar_empleos()
sesion.exportar_datos_json()
sesion.cerrar_session()

driver.quit()
