### Main File is Rec_App.py

## Notas para David:
**a**- NO pude solucionar mi problema con la creación del conjunto de siguientes, por lo que no es seguro si gramáticas Q o LL(1) queden bien. El programa no fallará, pero posiblemente el autómata y el reconocedor no estén correctos.
**b-** No ingreses gramáticas con demasiadas producciones, Tkinter no permite ponerle scroll a los frames. Podras navegar pero a ciegas y con el tabulador. Quizas logré arreglar esto.
**c-** Preferiblemente usa la aplicación en el tamaño por defecto o maximizado. Por las mismas razones del punto anterior.


# Manual de Usuario:
En el botón "?" en la esquina superior izquierda se encuentran estas mismas instrucciones.

**1-** El primer paso es determinar el número de producciones de la gramática. Ingrese el número en el cuadro de texto y presione 'Confirmar'.
**1.1-** En cualquier momento puede ingresar otro número de producciones y presionar para confirmar, pero esto borrara el contenido de los cuadros de texto de las producciones.
**2-** Ingrese las producciones.
**2.1-** Para los lados izquierdos de estas no es necesario encerrar el no terminal entre <>, el programa lo hace automáticamente. Si ingresa < S > el no terminal resultante es "<<\S\>>"
**3-** Presione el botón 'crear'. Esto mostrará el autómata de pila al lado izquierdo, sus operaciones en el medio, y el reconocedor de hileras al lado derecho.
**4-** Si se desea saber que tipo de gramática es presione el botón 'S? Q? LL?'.
**5-** Para reconocer una hilera ingrésela en el cuadro de texto a la derecha de la aplicación y precione 'Pertenece?' Debajo de este se mostrará el resultado.
**6-** Si desea probar otra gramática presione 'Crear Nueva Gramatica', esto lo devolverá a la pantalla inicial.
 
First time coding in python. It's awesome!! :D
No technical manual since I don't know yet the equivalent of Javadoc for Python, but most of the code it's commented.
