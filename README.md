# Grupo 9

### Integrantes:

| Nombre y Apellido              |      Mail                      |     usuario Gitlab   |
| -----------------------------  | ------------------------------ | -------------------  |
|Alejandro Gareca                | gereca20jorge@gmail.com        | AleGareca            |
|Alan Martinez                   | alanmartinezunq@gmail.com      | @AlanMartinez93      |



# Practica 1

OK


# Practica 2

Esta Bien, funciona... pero les hago una acotacion para ir entendiendo la proxima practica:
(en esta practica la solucion es buena, pero la idea es que entiendan que implicancias tiene)

El estado en el handler está de más (y en algún punto podria llegar a generar problemas).
```
    def setStatePrograms(self,bool):
        self._state = bool
```

La idea es que la interrupcion se va  llamar en distintos momentos (y para distintos procesos)... en el futuro no vamos a tener un solo proceso "corriendo", 
por lo tanto la pregunta de que si hay que seguir corriendo otros procesos (o no) la deberíamos hacer en el momento que se esta ejecutando el Kill (y no antes)

Piensen la interrupcion algo asi:

```
        if(not self.kernel.q.empty()):
            self.kernel.next()
        else:
            log.logger.info("Batch Finished")
            HARDWARE.switchOff()
```
no cambien el codigo... pero hagan el ejercicio de pensarlo así... no se que paso desde que mandé a correr el proceso y su finalizacion... por lo tanto no puedo "cachear" el estado del S.O. en un estado de la interrupcion


# Practica 3

Correcciones por aplicar en la practica 4:

Intente evitar calcular los parámetros (llamando a otros métodos) en la llamada a un método, las ejecuciones sen línea no siempre son claras, prefiero que se defina una variable y se inicialice esta con la evaluación del método que calcula el valor para luego pasar esta variable como parámetro, es más claro para entender que hace y ayuda al momento de hacer debugging del código. 

Esto se puede ver en la creación del PCB en la IRQ de NEW, utilizaría variables para signar los valores de pid y dirección base.

Además, evita errores como el que podemos ver en el siguiente código, donde el PID informado en el log es diferente al asignado al PCB:
```
        pcbNew = PCB(self.kernel.pcbTable.getNewPid(), Process.NEW, irq.parameters.name, self.kernel.loader.load_program(irq.parameters))
        log.logger.info(self.kernel.pcbTable.getNewPid())
```
La PCBTable está sobrecargada de responsabilidad, por ejemplo, el método setOnPcbRunning no debería asignar el estado al PCB, es preferible para que el código sea más entendible hacer el cambio de estado en el handler, este mismo problema se ve en otros métodos de la clase. Pensando en tener clases con responsabilidades acotadas, y si es realmente son necesarios estos métodos, los movería a kernel, aunque algunos de ellos se podrías evitar. 

Eliminar el metodo changeStateRunningPcb y manejar el cambio de estado en cada handler. 

Con respecto al Dispatcher, tengo una duda. Es realmente necesario que el save realice un update del pcb? no debería ser actualizado por ser una referencia a un objecto?
Intentar eliminar el método updatePcb de la PCBTable.

El objetivo de esta practica es que mirando cada Handler se pueda  entender todo lo que sucede al manejar cada IRQ.



# Practica 4

Excelente la idea de organizar del código en carpetas, lo único que noto es que tenemos carpetas con 1 sola clase y eso a veces es contraproducente, 
tal vez podamos pensar en carpetas que agrupen clases en base a su funcionalidad. 
Por ejemplo, el folder Scheduler tiene un solo file con todas las clases, esperaría que si decidí separarlo en folders, cada clase este en un file separado.

Intentar utilizar el idioma ingles siempre, por ejemplo, en los nombres de las clases DescripcionPorTick y DiagramaGantt. 
Lo mismo aplica a los métodos como en el caso de esExpropiar en los schedulers.

Siempre intentamos tener alta cohesión y bajo acoplamiento en nuestras clases, no veo una necesidad que la clase ReadyQueue tenga una referencia a un kernel.

La interrupción de IOOUT debería tener la lógica de expropiación.

Si en una clase abstracta define un método abstracto, las subclases deberían implementarlo por claridad.

Por favor apliquen los cambios.

# Practica 5
OK


Si bien la practica esta bien es un poco tedioso recorrer el código y sigo sin convencerme de la idea de tener carpetas con 1 solo archivo para organizarlo, sin dudas me movería a una organización por funcionalidad evitando carpetas con un solo archivo.
Estas clases por ejemplo podría estar juntas:
https://gitlab.com/so-unq-2020-s1/grupo_9/-/blob/master/practica_5/SistemaOperativo/PageTable/PageTable.py#L4
https://gitlab.com/so-unq-2020-s1/grupo_9/-/blob/master/practica_5/SistemaOperativo/MemoryManager/MemoryManager.py#L1

Acá hay 3 buenos ejemplos de un corte funcional, pero si en su interior la carpeta tuviera directamente las clases:
https://gitlab.com/so-unq-2020-s1/grupo_9/-/tree/master/practica_5/SistemaOperativo/Schedule  en este caso usaría el plural Schedulers
https://gitlab.com/so-unq-2020-s1/grupo_9/-/tree/master/practica_5/SistemaOperativo/InterruptionHandler en este caso usaría el plural InterruptionHandlers
https://gitlab.com/so-unq-2020-s1/grupo_9/-/tree/master/practica_5/SistemaOperativo/Gantt

Se nota el intento de prolijidad en el código, pero en este caso simplificaría el cálculo del new pid con un simple contador, a veces menos, es más.
https://gitlab.com/so-unq-2020-s1/grupo_9/-/blob/master/practica_5/SistemaOperativo/PcbTable/PCBTable.py#L22

Estos métodos no son necesarios, en este caso, usar la variable facilita la lectura y simplifica el código:
https://gitlab.com/so-unq-2020-s1/grupo_9/-/blob/master/practica_5/SistemaOperativo/Loader/Loader.py#L69
https://gitlab.com/so-unq-2020-s1/grupo_9/-/blob/master/practica_5/SistemaOperativo/Loader/Loader.py#L72

Me gustaría ver estos cambios aplicados o una muy buena justificación para no hacerlo.


