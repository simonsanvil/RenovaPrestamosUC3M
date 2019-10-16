# RenovadorLibrosUC3M
Aplicacion que renueva automaticamente tus prestamos de biblioteca de la Universidad Carlos III de Madrid.

**Instrucciones:**
1. Ejecuta el script desde una consola o desde tu IDE preferido (Spyder, PyCharm, VSC...)
2. Introduce tus credenciales de la UC3M en el formulario generado por el programa. 
3. Presiona "Renovar Prestamos".
4. Espera a que el programa culmine su tarea. Al acabar deberias ver la informacion acerca de tus renovaciones en el cuadro de texto
situado en la parte de abajo del formulario. De haber algun error, sigue las intrucciones de ese cuadro. 
5. Cierra el formulario una vez hayas acabado. 

**Requiere:** 
- Python version 3.0 o mayor + pip.
- Un usuario de Biblioteca UC3M (El NIA es valido).
- La contraseña asociada a dicho usuario. 

**PARA RENOVAR SIN NECESIDAD DE INTRODUCIR TUS CREDENCIALES CADA VEZ QUE EJECUTES EL PROGRAMA:**
1. Crea un archivo de texto *.txt* (usando Notepad, por ejemplo).
2. En la primera linea escribe tu nombre de usuario de bilioteca de la UC3M. (NIA, StudentID, ISIC,...)
3. En la segunda linea escribe la contraseña asociada a dicho usuario.
_______________
 **Ejemplo:** 
 
 *100123456*      
                
 *contraseña*

***Nota: Ni tu usuario ni tu contraseña es enviado a un sitio ajeno al sitio oficial de la Biblioteca y no puede ser vista por desalloradores ni por terceros.***
______________
4. Guarda el archivo en la carpeta donde se encuentra el script con el nombre "AulaCredentials".
5. Cuando vuelvas a ejecutar el programa notaras que no te pedira tus credenciales usando el formulario.
Nota: Para rehabilitar el formulario solo tienes que eliminar el archivo "AulaCredentials.txt" de la carpeta donde se encuentra el programa o moverlo a alguna otra ubicacion. 

*Para mayor automatizacion prueba usando aplicaciones como Windows Task Scheduler o Chron para programar la ejecucion del script cada cierto tiempo.* 

