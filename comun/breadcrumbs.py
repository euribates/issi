#!/usr/bin/env python3

from typing import Any

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class BreadCrumb():
    """Clase para generar *breadcrumbs*.

    Cada nodo de tipo ``BreadCrumb`` apunta al anterior, hasta llegar al
    nodo raiz. Se crea una variable global ``ROOT`` para tener el inicio
    de todos los *breadcrumbs*. Podemos añadir un nuevo *breadcrumb*
    llamando al método ``step`` del padre.

    La idea es ir creado paso a paso el *breadcrumb*, y luego, al
    imprimirlo, se muestran en orden inverso, de forma que el primero
    será el nodo ``ROOT``.

    Hay una plantilla en ``main/templates/includes/breadcrumbs.html`` 
    para mostrar el *breadcrumb* en formato bootstrap 5.
    """
    
    def __init__(self, label: str, url: str, *args, **kwargs):
        '''Constructor de nodos del *breadcrumb*.

        La idea es que esta llamada solo se realiza una vez, para
        crear el nodo ``ROOT``. El resto de los nodos se crean
        llamando al metodo ``step`` del nodo anterior al que
        se quiere crear, que llamará a este método.

        Parameters:
            
            - label (str): Etiqueta de texto que se muestra para
              idetificar el paso.

            - url (str): Enlace a usar. Se enlazan todos los
              pasos, excepto el último, ya que se entiende que
              sería la misma página en la que estamos.

            - *args (list): Si se indica parámetros posicionales extra,
              estos se usaran para calcular el URL de forma
              dinámica.
    
            - **kwargs (dict): Si se indica parámetros nominales extra,
              estos se usaran para calcular el URL de forma
              dinámica.
        '''

        self.parent = None
        if hasattr(label, 'get_absolute_url') and not url:
            url = label.get_absolute_url()
        self.label = str(label)
        self._url = url
        self.args = args
        self.kwargs = kwargs
        self.chain = []

    def __len__(self) -> int:
        '''Total de pasos actualmente incluidos en el *breadcrumb*.

        Returns:

            (int) Número total de pasos (incluyendo el nodo actual)
        '''
        counter = 1
        current = self
        while current.parent is not None:
            counter += 1
            current = current.parent
        return counter

    def _get_url(self) -> str:
        '''Obtiene el url de cada paso.

        Tiene que ser calculado dinámicamente, ya que pueden
        usarse valores pasados como parámetros posicionales
        o nominales para obtener la dirección final.

        La URL final se calcula usando ``reverse``, y pasandole
        los parámetros posibcionales y/o nominales que se le
        hayan pasado al constructor.

        Además, y de forma alternativa, si se le pasó en el
        parámetro de creación ``url`` un objeto con un método
        que se llame ``get_absolute_url``, y si dicho método no
        acepta ningún parámetro, se usara ese método para obtener
        la URL. En este caso no se tendrán en cuenta los 
        parámetros almacenados.

        Returns:

            (str): La URL vinculada al paso actual.
        '''
        if (
            self._url
            and not self.args
            and not self.kwargs
            and hasattr(self._url, "get_absolute_url")
            and callable(self._url.get_absolute_url)
        ):
            return self._url.get_absolute_url()
        try:
            return reverse(
                self._url,
                args=self.args,
                kwargs=self.kwargs,
                )
        except NoReverseMatch:
            return self._url

    url = property(_get_url)

    def __getitem__(self, index: int) -> Any:
        '''Permite acceder a un paso del *breadcrumb* como una tupla.

        Solo se puede acceder de esa manera a las posiciones 0 (texto
        descriptivo) y al 1 (URL).
        '''
        if index == 0:
            return self.label
        if index == 1:
            return self.url
        raise IndexError(
            "La clase BreadCrumb "
            "solo se puede acceder con índices 0, 1"
            )

    def __iter__(self):
        '''Iterador que recorre todos los pasos del *breadcrumb*.

        Devuelve un iterador para obtener todos los pasos
        desde el nodo actual (``self``) hasta el nodo raiz.

        Returns:

            (Iterator): Iterador que recorre los nodos ascendentes
            del nodo actual, hasta llegar a la raiz.
        '''
        item = self
        self.chain = [item]
        while item.parent:
            item = item.parent
            self.chain.append(item)
        return self

    def __next__(self):
        '''Implementación de __next__ para el iterador.
        '''
        while self.chain:
            item = self.chain.pop()
            return item
        raise StopIteration

    def step(self, label, url=None, *args, **kwargs):
        '''Ańadir un nuevo paso al *breadcrumbs*.

        Esta función crea un nuevo nodo de tipo ``BreadCrumb``, y
        lo ańade como hijo del nodo actual. Es la forma normal
        de ir creado el *breadcrumb*. devuelve el nuevo nodo
        de forma que se puede usar encadenando las llamadas.

        Parameters:
            
            - label (str): Etiqueta de texto que se muestra para
              idetificar el paso.

            - url (str): Enlace a usar. Se enlazan todos los
              pasos, excepto el último, ya que se entiende que
              sería la misma página en la que estamos.

            - *args (list): Si se indica parámetros posicionales extra,
              estos se usaran para calcular el URL de forma
              dinámica.
    
            - *kwargs (dict): Si se indica parámetros nominales extra,
              estos se usaran para calcular el URL de forma
              dinámica.
        
        Returns:

            (BreadCrumb): El nuevo nodo añadido.

        '''
        new_breadcrumb = BreadCrumb(label, url, *args, **kwargs)
        new_breadcrumb.parent = self
        return new_breadcrumb

    def __str__(self):
        '''Representación textual del *breadcrumb*.

        Todos los nodos elnazan con el correspondiente URL, excepto el
        último, ya que se entiende que sería la misma página en la que
        estamos.

        Parameters:

            self (BreadCrumb): El paso actual del *breadcrumb*.

        Returns:

            (str): Texto HTML del paso del *breadcrumb* actual

        '''
        *items, last = list(iter(self))
        buff = []
        for label, url in items:
            buff.append(f'<a href="{url}">{label}</a>')
        buff.append(f"<strong>{label}</strong>")
        return '\n'.join(buff)


HOME = BreadCrumb(
    '<i class="bi bi-house-door-fill"></i>',
    'https:/www.gobiernodecanarias.org/',
    )

INTRANET = HOME.step(
    'Intranet',
    'https://www.gobiernodecanarias.net/',
    )

APPS = INTRANET.step('Apps', '#')
