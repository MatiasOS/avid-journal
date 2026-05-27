# PAPER_INDEX — Ayrton Porto Tesis

Base de datos local de bloques formalizados de este paper.
El Sketch Agent debe consultar este archivo ANTES de buscar en Mathlib.

---

## def:lenguaje-algebraico
Type: definition
Status: ✅ verified
File: Paper.lean:12
Depends on: —
Statement: Un lenguaje algebraico (o tipo algebraico) es un par \( (\mathcal{L},\mathrm{ar}) \), donde \( \mathcal{L} \) es un conjunto de símbolos y \( \mathrm{ar}\colon \mathcal{L}\to\mathbb{N}_{0} \) es una f...

---

## def:algebra
Type: definition
Status: ✅ verified
File: Paper.lean:21
Depends on: —
Statement: Un álgebra \( \mathbf{A} \) de tipo \( \mathcal{L} \) es un par \( \mathbf{A}=(A,\mathcal{L}) \), donde \( A \) es un conjunto no vacío, el cual llamaremos universo, y para cada símbolo \( f\in\mathca...

---

## def:subalgebra
Type: definition
Status: ✅ verified
File: Paper.lean:33
Depends on: —
Statement: Sean \( \mathbf{A},\mathbf{B} \) álgebras de tipo \( \mathcal{L} \). Diremos que \( \mathbf{B} \) es una subálgebra de \( \mathbf{A} \) si \( B\subseteq A \) y para toda operación \( f\in\mathcal{L} \...

---

## def:homomorfismo
Type: definition
Status: ✅ verified
File: Paper.lean:44
Depends on: —
Statement: Una función \( \alpha\colon A\to B \) es un homomorfismo de álgebras si para toda operación \( f\in\mathcal{L} \) de aridad \( n \) y todo \( a_{1},\dots,a_{n}\in A \) se cumple \[ \alpha(f^{\mathbf{A...

---

## def:producto-algebras
Type: definition
Status: ✅ verified
File: Paper.lean:73
Depends on: —
Statement: Sea \( I \) un conjunto de índices y \( \{\mathbf{A}_{i}\}_{i\in I} \) una familia de álgebras del mismo tipo. Su producto \( \prod_{i\in I}\mathbf{A}_{i} \) es el álgebra de universo \( \prod_{i\in I...

---

## def:topologia
Type: definition
Status: ✅ verified
File: Paper.lean:91
Depends on: —
Statement: Sea \( X \) un conjunto no vacío.  Una topología sobre \( X \) es una familia \( \tau \subseteq \mathcal{P}(X) \) que cumple: \begin{enumerate}  \item \( \emptyset,\, X \in \tau \);  \item si \( \{U_i...

---

## def:clausura-interior
Type: definition
Status: ✅ verified
File: Paper.lean:109
Depends on: —
Statement: Sea \( (X,\tau) \) un espacio topológico y \( A\subseteq X \). La clausura de \( A \) en \( (X,\tau) \) se define como \[ Cl_{\tau}(A)  = \bigcap \{V \subseteq X : A\subseteq V,\ V \text{ es cerrado}\...

---

## def:base-generadora
Type: definition
Status: ✅ verified
File: Paper.lean:120
Depends on: —
Statement: Sea $X$ un conjunto no vacío. Una familia $\mathcal{B}\subseteq\mathcal{P}(X)$ se dice base para una topología en $X$ si satisface:  \begin{enumerate}  \item $\displaystyle \bigcup_{B\in\mathcal{B}} B...

---

## def:base-espacio
Type: definition
Status: ✅ verified
File: Paper.lean:141
Depends on: —
Statement: Sea $(X,\tau)$ un espacio topológico. Una familia $\mathcal{B}\subseteq\tau$ se dice base de $(X,\tau)$ si cumple:  \begin{enumerate}  \item $\mathcal{B}\subseteq\tau$;  \item para todo $U\in\tau$ y t...

---

## def:subbase
Type: definition
Status: ✅ verified
File: Paper.lean:156
Depends on: —
Statement: Una subbase para una topología \( \tau \) sobre \( X \) es una familia \( \mathscr{S}\subseteq\mathcal{P}(X) \) tal que \( \bigcup_{S\in\mathscr{S}} S = X \). La topología generada por \( \mathscr{S}...

---

## def:cubrimiento-abierto
Type: definition
Status: ✅ verified
File: Paper.lean:174
Depends on: —
Statement: Sea $(X,\tau)$ un espacio topológico.  Una familia $\{U_i\}_{i\in I}\subseteq\tau$ se denomina  cubrimiento abierto de $X$ si \[ X = \bigcup_{i\in I} U_i. \]

---

## def:compacidad
Type: definition
Status: ✅ verified
File: Paper.lean:185
Depends on: —
Statement: Un espacio topológico $(X,\tau)$ es compacto si  para todo cubrimiento abierto $\{U_i\}_{i\in I}$ de $X$  existe un subcubrimiento finito, es decir, \[ X = U_{i_1}\cup\cdots\cup U_{i_n} \quad\text{par...

---

## def:compacidad-subespacio
Type: definition
Status: ✅ verified
File: Paper.lean:195
Depends on: —
Statement: Sea $(X,\tau)$ un espacio topológico y $V\subseteq X$ un subespacio con la topología inducida $\tau_V$.  Decimos que $V$ es compacto si $(V,\tau_V)$ es compacto.

---

## block_14 — {\cite[Lema~26.1
Type: lemma
Status: ⚠️ axiom
File: Paper.lean:202
Depends on: —
Source: {\cite[Lema~26.1
Statement: {Munkres}}]\label{lem:compacto-subespacio-Munkres} Sean $(X,\tau)$ un espacio topológico y $V \subseteq X$. Las siguientes afirmaciones son equivalentes: \begin{enumerate}  \item $(V,\tau_{V})$ es un ...

---

## def:espacios-T
Type: definition
Status: ✅ verified
File: Paper.lean:206
Depends on: —
Statement: Sea \( (X,\tau) \) un espacio topológico.  Diremos que: \begin{itemize}  \item \( (X,\tau) \) es \(T_0\) si para cualesquiera \( x\ne y\in X \)  existe \( U\in\tau \) tal que \( x\in U,\, y\notin U \)...

---

## def:continuidad-homeomorfismo
Type: definition
Status: ✅ verified
File: Paper.lean:228
Depends on: —
Statement: Sean $(X,\tau)$ y $(Y,\tau')$ espacios topológicos y  $f\colon X\to Y$ una función. Diremos que $f$ es continua si, para todo abierto  $U\in\tau'$, la preimagen $f^{-1}[U]$ es un abierto de $(X,\tau)$...

---

## def:categoria
Type: definition
Status: ✅ verified
File: Paper.lean:250
Depends on: —
Statement: Una categoría \( \mathsf{C} \) consta de los siguientes datos: \begin{enumerate}[\normalfont (1)]  \item una colección denominada \( Ob(\mathsf{C}) \), cuyos elementos se llaman objetos;  \item una co...

---

## block_18
Type: definition
Status: ✅ verified
File: Paper.lean:273
Depends on: —
Statement: Sea \( \mathsf{C} \) una categoría y \( f\colon x\to y \) un morfismo.  Se dice que \( f \) es un isomorfismo si existe un morfismo \( g\colon y\to x \) tal que \[ g\circ f=\Id_{x},\qquad f\circ g=\Id...

---

## block_19
Type: definition
Status: ✅ verified
File: Paper.lean:298
Depends on: —
Statement: A toda categoría \( \mathsf{C} \) se le asocia su categoría opuesta \( \mathsf{C}^{op} \), que posee los mismos objetos y los mismos morfismos, pero con las direcciones invertidas.  Formalmente, \[ \m...

---

## block_20
Type: definition
Status: ✅ verified
File: Paper.lean:317
Depends on: —
Statement: Sea $\mathsf{C}$ una categoría.  Una subcategoría $\mathsf{D}$ de $\mathsf{C}$ consta de:  \begin{enumerate}[\normalfont (a)]  \item una colección de objetos $\mathrm{Ob}(\mathsf{D})$, donde cada obje...

---
## def: funtor
Type: definition
Status: ✅ verified
File: Paper.lean:339
Depends on: —
Statement: Sean \( \mathsf{C} \) y \( \mathsf{D} \) categorías. Un funtor covariante es un mapeo \( F\colon\mathsf{C}\to\mathsf{D} \) que asigna: \begin{enumerate}[\normalfont (1)]  \item a cada objeto \( x \) d...

---

## block_22
Type: definition
Status: ✅ verified
File: Paper.lean:369
Depends on: —
Statement: Dada una categoría \( \mathsf{C} \), se define el funtor identidad \[ \mathrm{I}_{\mathsf{C}}\colon \mathsf{C}\to\mathsf{C}, \qquad \mathrm{I}_{\mathsf{C}}(x)=x,\quad \mathrm{I}_{\mathsf{C}}(f)=f. \]

---

## def:transf-nat
Type: definition
Status: ✅ verified
File: Paper.lean:379
Depends on: —
Statement: Sean $F,G \colon \mathsf{C} \to \mathsf{D}$ dos funtores covariantes.  Una transformación natural $\theta \colon F \Rightarrow G$ es una asignación que a cada objeto $X$ de $\mathsf{C}$ le asocia un m...

---

## block_24
Type: definition
Status: ✅ verified
File: Paper.lean:402
Depends on: —
Statement: Sean \( \mathsf{C} \) y \( \mathsf{D} \) categorías. Una equivalencia de categorías entre \( \mathsf{C} \) y \( \mathsf{D} \) está dada por un par de funtores covariantes \[ F\colon\mathsf{C}\to\maths...

---

## def:equivalencia-dual
Type: definition
Status: ✅ verified
File: Paper.lean:439
Depends on: —
Statement: Sean \( \mathsf{C} \) y \( \mathsf{D} \) dos categorías. Diremos que \( \mathsf{C} \) y \( \mathsf{D} \) son dualmente equivalentes si existe una equivalencia de categorías entre \( \mathsf{C} \) y \(...

---

## def:isomorfismo-categorias
Type: definition
Status: ✅ verified
File: Paper.lean:445
Depends on: —
Statement: Sean \( \mathsf{C} \) y \( \mathsf{D} \) dos categorías. Decimos que \( \mathsf{C} \) y \( \mathsf{D} \) son isomorfas si existen funtores \[ F\colon \mathsf{C} \longrightarrow \mathsf{D}, \qquad G\co...

---

## block_27
Type: definition
Status: ✅ verified
File: Paper.lean:464
Depends on: —
Statement: Un retículo es un álgebra \( \mathbb{L}=(L,\wedge,\vee) \) de tipo \((2,2)\) tal que, para cualesquiera \( a,b,c \in L \), se cumplen las siguientes igualdades: \begin{enumerate}[\normalfont (1)]  \it...

---

## block_28
Type: definition
Status: ❌ failed
File: Paper.lean:470
Depends on: —
Statement: Un retículo \( \mathbb{L}=(L,\wedge,\vee) \) posee un primer elemento (o elemento inferior) si existe \( 0 \in L \) tal que \( 0 \wedge a = 0 \) para todo \( a \).  De modo dual, posee un último eleme...

---

## def:reticulo_distributivo
Type: definition
Status: ❌ failed
File: Paper.lean:474
Depends on: —
Statement: Un retículo \( \mathbb{L}=(L,\wedge,\vee) \) es distributivo si para todo \( a,b,c \in L \) se cumple \[ a \wedge (b \vee c) = (a \wedge b) \vee (a \wedge c). \] Esta condición es equivalente a su for...

---

## def:filtro
Type: definition
Status: ❌ failed
File: Paper.lean:478
Depends on: —
Statement: Sea \( \mathbb{L}=(L,\wedge,\vee) \) un retículo.  Un subconjunto no vacío \( F \subseteq L \) se llama filtro si satisface: \begin{enumerate}[\normalfont (1)]  \item \( F \) es creciente con respecto...

---
