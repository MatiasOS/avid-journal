# REVIEW — Ayrton Porto Tesis

Documento de seguimiento humano. El orchestrator anota aqui los bloques que
necesitan revisar manualmente: axiomas declarados (resultados externos sin
prueba en el paper) y bloques que no se pudieron formalizar (failed).

Los bloques `verified` NO aparecen aqui; vive el log limpio en `PAPER_INDEX.md`.

---

## Axiomas declarados


### `block_14` (lemma) — {\cite[Lema~26.1
- **Paper.lean**: linea 202
- **Fuente**: {\cite[Lema~26.1
- **Enunciado**:

```
{Munkres}}]\label{lem:compacto-subespacio-Munkres}
Sean $(X,\tau)$ un espacio topológico y $V \subseteq X$. Las siguientes afirmaciones son equivalentes:
\begin{enumerate}
 \item $(V,\tau_{V})$ es un subespacio compacto.
 \item Para todo cubrimiento $\{U_{i}\}_{i \in I}$ de $V$ por $\tau$-abiertos, 
 existe un subcubrimiento finito $U_{i_1},\dots,U_{i_n}$ de $\tau$-abiertos de $V$.
\end{enumerate}
```

---

## Bloques fallidos
















### `def:espacios-T` (definition)
- **Paper.lean**: linea 206
- **Enunciado**:

```
Sea \( (X,\tau) \) un espacio topológico. 
Diremos que:
\begin{itemize}
 \item \( (X,\tau) \) es \(T_0\) si para cualesquiera \( x\ne y\in X \)
 existe \( U\in\tau \) tal que \( x\in U,\, y\notin U \)
 o bien \( y\in U,\, x\notin U \);
 \item \( (X,\tau) \) es \(T_1\) si para cualesquiera \( x\ne y\in X \)
 existen abiertos \( U,V\in\tau \) con \( x\in U,\ y\notin U \)
 y \( y\in V,\ x\notin V \);
 \item \( (X,\tau) \) es \(T_2\) (o Hausdorff)
 si para todo \( x\ne y\in X \) existen \( U,V\in\tau \)
 con \( x\in U \), \( y\in V \) y \( U\cap V=\emptyset \).
\end{itemize}
```

### `def: funtor` (definition)
- **Paper.lean**: linea 340
- **Enunciado**:

```
Sean \( \mathsf{C} \) y \( \mathsf{D} \) categorías.
Un funtor covariante es un mapeo \( F\colon\mathsf{C}\to\mathsf{D} \) que asigna:
\begin{enumerate}[\normalfont (1)]
 \item a cada objeto \( x \) de \( \mathsf{C} \), un objeto \( F(x) \) de \( \mathsf{D} \);
 \item a cada morfismo \( f\colon x\to y \) de \( \mathsf{C} \), un morfismo \( F(f)\colon F(x)\to F(y) \) de \( \mathsf{D} \);
\end{enumerate}
que preserva identidades y composición, es decir:
\[
F(\Id_{x})=\Id_{F(x)},
\qquad
F(g\circ f)=F(g)\circ F(f).
\]
Si \( F \) invierte la dirección de los morfismos, de manera que
de un morfismo  ...
```

### `block_22` (definition)
- **Paper.lean**: linea 344
- **Enunciado**:

```
Dada una categoría \( \mathsf{C} \), se define el funtor identidad
\[
\mathrm{I}_{\mathsf{C}}\colon \mathsf{C}\to\mathsf{C},
\qquad
\mathrm{I}_{\mathsf{C}}(x)=x,\quad \mathrm{I}_{\mathsf{C}}(f)=f.
\]
```

### `def:transf-nat` (definition)
- **Paper.lean**: linea 348
- **Enunciado**:

```
Sean $F,G \colon \mathsf{C} \to \mathsf{D}$ dos funtores covariantes. 
Una transformación natural $\theta \colon F \Rightarrow G$
es una asignación que a cada objeto $X$ de $\mathsf{C}$ le
asocia un morfismo
\[
\theta_X \colon F(X) \longrightarrow G(X)
\]
en la categoría $\mathsf{D}$, de manera tal que para cada
morfismo $f \colon X \to Y$ en $\mathsf{C}$, el siguiente diagrama conmuta:
\[
\begin{tikzcd}
F(X) \arrow[r, "\theta_X"] \arrow[d, "F(f)"'] &
G(X) \arrow[d, "G(f)"] \\
F(Y) \arrow[r, "\theta_Y"'] &
G(Y).
\end{tikzcd}
\]
Es decir, 
\[
G(f)\circ \theta_X \;=\; \theta_Y \circ F(f).
\]
```

### `block_24` (definition)
- **Paper.lean**: linea 352
- **Enunciado**:

```
Sean \( \mathsf{C} \) y \( \mathsf{D} \) categorías.
Una equivalencia de categorías entre \( \mathsf{C} \) y \( \mathsf{D} \)
está dada por un par de funtores covariantes
\[
F\colon\mathsf{C}\to\mathsf{D},
\qquad
G\colon\mathsf{D}\to\mathsf{C},
\]
y por dos transformaciones naturales
\[
\theta\colon \mathrm{I}_{\mathsf{C}}\Rightarrow G\circ F,
\qquad
\phi\colon \mathrm{I}_{\mathsf{D}}\Rightarrow F\circ G,
\]
tales que cada morfismo componente \( \theta_{C} \) y \( \phi_{D} \) es un isomorfismo.
En este caso se dice que \( \mathsf{C} \) y \( \mathsf{D} \) son equivalentes.
```

### `def:equivalencia-dual` (definition)
- **Paper.lean**: linea 356
- **Enunciado**:

```
Sean \( \mathsf{C} \) y \( \mathsf{D} \) dos categorías.
Diremos que \( \mathsf{C} \) y \( \mathsf{D} \) son dualmente equivalentes
si existe una equivalencia de categorías entre \( \mathsf{C} \) y \( \mathsf{D}^{op} \) (o entre \( \mathsf{C}^{op} \) y \( \mathsf{D} \)). En este caso se dice que \( \mathsf{C} \) y \( \mathsf{D} \) son categorías duales.
```

### `def:isomorfismo-categorias` (definition)
- **Paper.lean**: linea 360
- **Enunciado**:

```
Sean \( \mathsf{C} \) y \( \mathsf{D} \) dos categorías.
Decimos que \( \mathsf{C} \) y \( \mathsf{D} \) son isomorfas
si existen funtores
\[
F\colon \mathsf{C} \longrightarrow \mathsf{D},
\qquad
G\colon \mathsf{D} \longrightarrow \mathsf{C},
\]
tales que se cumplen las igualdades estrictas
\[
F\circ G = \mathrm{I}_{\mathsf{D}},
\qquad
G\circ F = \mathrm{I}_{\mathsf{C}}.
\]
En este caso se escribe
\[
\mathsf{C}\;\cong\;\mathsf{D}.
\]
```

### `block_27` (definition)
- **Paper.lean**: linea 364
- **Enunciado**:

```
Un retículo es un álgebra \( \mathbb{L}=(L,\wedge,\vee) \) de tipo \((2,2)\) tal que, para cualesquiera \( a,b,c \in L \), se cumplen las siguientes igualdades:
\begin{enumerate}[\normalfont (1)]
 \item \( a \wedge (b \wedge c) = (a \wedge b) \wedge c \) y \( a \vee (b \vee c) = (a \vee b) \vee c \);
 \item \( a \wedge b = b \wedge a \) y \( a \vee b = b \vee a \);
 \item \( a \wedge a = a \) y \( a \vee a = a \);
 \item \( a \wedge (b \vee a) = a \) y \( a \vee (b \wedge a) = a \).
\end{enumerate}
```

### `block_28` (definition)
- **Paper.lean**: linea 368
- **Enunciado**:

```
Un retículo \( \mathbb{L}=(L,\wedge,\vee) \) posee un primer elemento (o elemento inferior) si existe \( 0 \in L \) tal que \( 0 \wedge a = 0 \) para todo \( a \). 
De modo dual, posee un último elemento (o elemento superior) si existe \( 1 \in L \) tal que \( a \vee 1 = 1 \) para todo \( a \). 
Cuando existen ambos, se dice que el retículo es acotado.
```

### `def:reticulo_distributivo` (definition)
- **Paper.lean**: linea 372
- **Enunciado**:

```
Un retículo \( \mathbb{L}=(L,\wedge,\vee) \) es distributivo si para todo \( a,b,c \in L \) se cumple
\[
a \wedge (b \vee c) = (a \wedge b) \vee (a \wedge c).
\]
Esta condición es equivalente a su forma dual:
\[
a \vee (b \wedge c) = (a \vee b) \wedge (a \vee c).
\]
```

### `def:filtro` (definition)
- **Paper.lean**: linea 376
- **Enunciado**:

```
Sea \( \mathbb{L}=(L,\wedge,\vee) \) un retículo. 
Un subconjunto no vacío \( F \subseteq L \) se llama filtro si satisface:
\begin{enumerate}[\normalfont (1)]
 \item \( F \) es creciente con respecto al orden de \( \mathbb{L} \);
 \item si \( a,b \) pertenecen a \( F \), entonces \( a\wedge b \) también pertenece a \( F \)
 (es decir, \( F \) es cerrado bajo ínfimos).
\end{enumerate}
Un filtro \( F \) se dira propio si $F \neq L$, es decir, está propiamente contenido en \( L \).
```

### `block_27` (definition)
- **Paper.lean**: linea 466
- **Enunciado**:

```
Un retículo es un álgebra \( \mathbb{L}=(L,\wedge,\vee) \) de tipo \((2,2)\) tal que, para cualesquiera \( a,b,c \in L \), se cumplen las siguientes igualdades:
\begin{enumerate}[\normalfont (1)]
 \item \( a \wedge (b \wedge c) = (a \wedge b) \wedge c \) y \( a \vee (b \vee c) = (a \vee b) \vee c \);
 \item \( a \wedge b = b \wedge a \) y \( a \vee b = b \vee a \);
 \item \( a \wedge a = a \) y \( a \vee a = a \);
 \item \( a \wedge (b \vee a) = a \) y \( a \vee (b \wedge a) = a \).
\end{enumerate}
```

### `block_28` (definition)
- **Paper.lean**: linea 470
- **Enunciado**:

```
Un retículo \( \mathbb{L}=(L,\wedge,\vee) \) posee un primer elemento (o elemento inferior) si existe \( 0 \in L \) tal que \( 0 \wedge a = 0 \) para todo \( a \). 
De modo dual, posee un último elemento (o elemento superior) si existe \( 1 \in L \) tal que \( a \vee 1 = 1 \) para todo \( a \). 
Cuando existen ambos, se dice que el retículo es acotado.
```

### `def:reticulo_distributivo` (definition)
- **Paper.lean**: linea 474
- **Enunciado**:

```
Un retículo \( \mathbb{L}=(L,\wedge,\vee) \) es distributivo si para todo \( a,b,c \in L \) se cumple
\[
a \wedge (b \vee c) = (a \wedge b) \vee (a \wedge c).
\]
Esta condición es equivalente a su forma dual:
\[
a \vee (b \wedge c) = (a \vee b) \wedge (a \vee c).
\]
```

### `def:filtro` (definition)
- **Paper.lean**: linea 478
- **Enunciado**:

```
Sea \( \mathbb{L}=(L,\wedge,\vee) \) un retículo. 
Un subconjunto no vacío \( F \subseteq L \) se llama filtro si satisface:
\begin{enumerate}[\normalfont (1)]
 \item \( F \) es creciente con respecto al orden de \( \mathbb{L} \);
 \item si \( a,b \) pertenecen a \( F \), entonces \( a\wedge b \) también pertenece a \( F \)
 (es decir, \( F \) es cerrado bajo ínfimos).
\end{enumerate}
Un filtro \( F \) se dira propio si $F \neq L$, es decir, está propiamente contenido en \( L \).
```

---

## Notas adicionales

## Axiomas declarados

(ninguno todavia)

---

## Bloques fallidos

(ninguno todavia)

---

## Notas adicionales
