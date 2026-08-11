# Business Data Analytics - Restaurant Analytics

## 1. Objetivo

El objetivo de este laboratorio es consolidar y analizar la información de ventas de un restaurante correspondiente a dos semanas de operación.

El análisis busca comparar el comportamiento semanal de los ingresos, identificar los productos con mayor aporte a los ingresos y frecuencia de compra, analizar la recurrencia de clientes y reconocer patrones agregados de consumo.

El análisis se limita a los ingresos y frecuencia de compra, debido a que los datos disponibles no contienen costos, cantidades ni descuentos.

## 2. Archivos utilizados

Para realizar el análisis se utilizaron los siguientes archivos:

* `Restaurant-Foods.csv`: catálogo de productos y precios unitarios.
* `Restaurant-Week1-Sales.csv`: registros de ventas correspondientes a la primera semana.
* `Restaurant-Week2-Sales.csv`: registros de ventas correspondientes a la segunda semana.
* `Restaurant-Customers.csv`: utilizado localmente para realizar las uniones y el análisis de clientes.

**Nota de privacidad:** el archivo `Restaurant-Customers.csv` no se incluye en el repositorio público debido a que contiene información de clientes.

## 3. Herramientas utilizadas

* Python
* Google Colab
* Pandas
* SQLite
* Matplotlib
* GitHub

## 4. Instrucciones de ejecución

1. Abrir el notebook `Restaurant_Analytics_Week2.ipynb`.
2. Cargar los archivos CSV requeridos.
3. Ejecutar las celdas del notebook en orden.
4. Verificar las validaciones de claves y referencias.
5. Ejecutar la consolidación de las tablas.
6. Ejecutar el cálculo de los indicadores.
7. Ejecutar la consulta SQL.
8. Revisar los gráficos y resultados obtenidos.

El archivo de clientes debe mantenerse fuera del repositorio público.

## 5. Principales hallazgos

Durante las dos semanas analizadas se registraron 250 ventas en cada semana.

Los ingresos de la semana 1 fueron de $1.962,68 y los de la semana 2 fueron de $1.923,88, presentando una disminución aproximada del 1,98 %. El ingreso promedio por registro pasó de $7,85 a $7,70.

En el análisis del menú, Steak presentó los mayores ingresos acumulados con $1.249,50. Pasta alcanzó $755,46 y Burrito $569,43.

La frecuencia de compra no es equivalente a los ingresos. Por ejemplo, Drink registró 59 compras, siendo uno de los productos con mayor frecuencia, pero sus ingresos fueron inferiores debido a su menor precio.

En cuanto a recurrencia, 46 clientes realizaron compras en ambas semanas, equivalente a una tasa de recurrencia del 20,81 %.

Los resultados por ocupación fueron analizados de manera agregada y no se utilizaron para realizar afirmaciones sobre clientes individuales.

## 6. Recomendación

Como acción prioritaria para la siguiente semana se propone implementar una estrategia de fidelización orientada a incrementar la recurrencia de compra.

Se recomienda utilizar el 20,81 % observado como línea base y medir nuevamente la tasa de recurrencia durante la siguiente semana. También se recomienda realizar seguimiento al desempeño de los productos con mayor aporte a los ingresos y de aquellos con mayor frecuencia de compra.

## 7. Limitaciones

El análisis corresponde únicamente a dos semanas de operación. Por esta razón, las variaciones observadas no permiten establecer tendencias de largo plazo ni atribuir causalidad a los cambios.

Además, los datos no contienen costos, cantidades ni descuentos, por lo que el análisis se limita a ingresos, frecuencia de compra y recurrencia.

No se publican nombres de clientes ni el archivo de clientes en el repositorio público.
