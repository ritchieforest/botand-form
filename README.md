# botand-form: Procesador de Texto a JSON para Formularios

**botand-form** es un procesador de texto diseñado para simplificar la creación y carga de formularios a partir de descripciones de texto. Este proyecto toma un texto de entrada y lo desfragmenta en un formato JSON estructurado, lo que facilita su uso en aplicaciones que requieren la captura y procesamiento de datos mediante formularios.


## Características

- **Desfragmentación de Texto**: Convierte descripciones textuales en objetos JSON claros y organizados.
- **Adaptación a Formularios**: El JSON generado es fácilmente integrable en sistemas de formularios, optimizando la carga de datos.
- **Configuración Flexible**: Permite ajustar los parámetros de desfragmentación según las necesidades del proyecto.

## Ejemplo de Uso

Dado un texto como: Me gustaria añadir un producto AFINADOR CROMATICO PINZA MCT6 de categoria MAGMA, que tenga el precio 5909.3 y el proveedor sea ALEYMAR, con un stock 383, con un codigo de proveedor 20 y el codigo interno para el producto 120500 para la marca MAGMA


**botand-form** generará un JSON como:

```json
{
  "producto": "AFINADOR CROMATICO PINZA MCT6",
  "categoria": "MAGMA",
  "precio": 5909.3,
  "proveedor":"ALEYMAR",
  "stock":383,
  "codigo_proveedor":"20",
  "codigo_interno":"120500",
  "marca":"MAGMA"
}
```json
![Imagen de Ejemplo botand-form](./ejemplo.jpeg)


