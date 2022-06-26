# Image-Search-Engine
Content-Based Image Retrieval System Implemented Using Python, Flask And OpenCV.
* Given a query image, this app returns other images from database in order of similar color content.
* Uses a color histogram to define the color content of an image, uses chi-squared distance to determine
how similar two image histograms are.

## Usage Guide
1. To use a different image dataset (optional)
    * Populate image DB in `app/static/images`
    * Then in Terminal: 
      ```bash
      >> python3 -m venv venv
      >> source venv/bin/activate
      >> pip install -r requirements.txt
      >> cd app
      >> python index.py --dataset static/images --index index.csv
      ```

2. Run locally using Docker
    * Install [Docker](https://docs.docker.com/install/#supported-platforms)
    * Then in Terminal:
      ```bash
      >> docker build --tag=imagesearch .
      >> docker run -p 80:8000 imagesearch
      ```
* You should be able to access app at `localhost:80` in browser


### Sources
* [pyimagesearch.com](https://www.pyimagesearch.com/start-here-learn-computer-vision-opencv/)
* [flask docs](http://flask.pocoo.org)
* [content-based image retrieval](https://en.wikipedia.org/wiki/Content-based_image_retrieval)


Project was made possible thanks to the many guides provided by [@Adrian Rosebrock](https://twitter.com/pyimagesearch) on [pyimagesearch.com](https://www.pyimagesearch.com/start-here-learn-computer-vision-opencv/)

### Introduction :

Avec la disponibilité d'un nombre croissant d'images numériques, il devient de plus en plus important de disposer d'un moyen efficace pour rechercher ces images. 
Les chercheurs sont toujours à la recherche de moyens pour rendre la recherche plus rapide et plus précise. L'une de ces techniques, la recherche d'images basée sur le contenu (CBIR). 
Cette technique développée dans les années 1980 a été introduite pour remplacer une autre technique qui consistait à annoter par du texte les images entrées dans une base de données. Ce processus d'annotation permettait à un utilisateur de retrouver une image en formulant une requête à l'aide de mots-clefs. Mais cette méthode trop subjective a été peu à peu abandonnée pour laisser la place à une méthode fondée sur l'interprétation du contenu de l'image. [1] 
CBIR est également connue sous le nom de Query By Image Content (QBIC), présente les technologies permettant d'organiser les images numériques par leurs caractéristiques visuelles. Ils sont basés sur l'application de techniques de vision par ordinateur au problème de récupération d'images dans de grandes bases de données. Content-Based Image Retrieval (CBIR) consiste à récupérer les images visuellement les plus similaires à une image de requête donnée à partir d'une base de données d'images. 
CBIR consiste à utiliser des caractéristiques telles que : 
-	La texture :  Dans une image, la texture est l'arrangement spatial, relativement répétitif et à une échelle assez petite pour ne pas se confondre avec la forme, des valeurs et des couleurs. La texture est un élément de l'aspect de surface. 
-	La couleur : est l’une des caractéristiques les plus importantes qui rendent possible la reconnaissance des images par les humains. La couleur est une propriété qui dépend de la réflexion de la lumière vers l'œil et du traitement de cette information dans le cerveau. Nous utilisons la couleur tous les jours pour faire la différence entre les objets, les lieux et l'heure de la journée. Habituellement, les couleurs sont définies dans des espaces colorimétriques tridimensionnels. Ceux-ci peuvent être RVB (rouge, vert et bleu), HSV (teinte, saturation et valeur) ou HSB (teinte, saturation et luminosité). Les deux derniers dépendent de la perception humaine de la teinte, de la saturation et de la luminosité.
-	La forme et la région : Une méthode de description particulièrement utilisée, Elle consiste à décrire une région en fonction des variations de courbure de son contour. Cette description est invariante en rotation et translation. Concernant le zoom, il faut a minima normaliser par la longueur du contour. Ces trois caractéristiques citées nous aident à trouver la photo souhaitée sans trop d'effort.
Avantages  de CBIR :

•	Plus pratique pour indexer et récupérer une grande quantité d'images.
•	Réduire les ambiguïtés liées à l'indexation.
•	Gains du temps.

Inconvénients de CBIR :


•	Les fonctionnalités de bas niveau ne sont pas capables de décrire et d'interpréter sémantiquement le contexte de l'image
•	Inutilisable pour les utilisateurs généraux. Car ils sont tenus de fournir une requête sous forme d'images
•	Il est limité par la taille de la base de données d'origine. S'il y a très peu d'images dans la base de données, alors... Elle ne renverra pas beaucoup de résultats.

La transformation en ondelettes :

Introduction :

L’analyse en ondelettes a été introduite au début des années 1980 . L’idée originale sur laquelle sont basées les ondelettes est apparue vers les années 1940 grâce au physicien Denis Gabor. La transformée en ondelette est un outil d’analyse puissant et complexe. 

Ils ont démontré leur force dans plusieurs domaines d’application tels que : Le dé bruitage, l’indexation, la compression, le codage…etc. 

Dans ce contexte les Ondelettes sont utilisées pour l’indexation d’images, ou encore la description de textures ou nous pouvons construire directement la signature des images. Car elle permet de concentrer l’information pertinente qu’elles contiennent d’où son utilisation en compression, dans la norme JPEG-2000... Nous rappelons dans ce qui suive les éléments principaux de la théorie des ondelettes. 

Nous ne pouvons pas parler de la transformée en ondelettes sans parler ou de commencer par la transformée de Fourier, car cette dernière une des principales raisons d’apparition de la première.

La transformée de Fourier (TF) et ses limitations :

La transformée de Fourier permet l’analyse fréquentielle d’un signal. Elle repose sur le fait que toute fonction périodique peut être représentée comme la somme d’une série de sinus et de cosinus dont on fait varier d’une part les amplitudes en les multipliant par des coefficients, et d’autre part les phases en les décalant de manière à ce qu’elles s’additionnent où se compensent. Le principe de la Transformée de fourier est donné dans la figure :
 
Figure : Transformée de Fourier 
La définition de la TF est donnée par la formule suivante :
 
Limitations de transformée de Fourier : son calcul nécessite la connaissance de toute l’histoire temporelle du signal. De plus, dans une transformée de Fourier, l’information sur le temps est présente (la transformée inverse donc possible), mais elle est cachée dans les phases : elle est en pratique impossible à extraire. On en est donc réduit à étudier un signal soit en fonction du temps, soit en fonction des fréquences qu’il contient, sans possibilité de conjuguer les deux analyses. La définition de la TF inverse est donnée par la formule :
 
Le passage à une transformée bidimensionnelle est donné par l’équation ci-dessous :
 
On peut utiliser la transformée de Fourier pour extraire des informations fréquentielles d’une image, toutefois le principal problème de la transformée de Fourier est son manque de résolution temporelle. Cela signifie simplement que si on est effectivement capable de détecter toutes les fréquences qui apparaissent dans un signal, on est en revanche incapable de déterminer à quel moment elles se produisent dans le signal. Il existe une transformée de Fourier plus « locale » donnant des informations mieux localisées, il s’agit de la transformée de Fourier Fenêtré (STFT).

Transformée de Fourier Fenêtrée (STFT) et sa limitation :

Une nouvelle méthode d’analyse est donc introduite pour pallier le manque d’information sur le temps dans la transformée de Fourier : elle utilise une « Fenêtre glissante ». Cette méthode, pouvant être adaptée aux signaux non-stationnaires, est très proche de l’analyse spectrale : on définit une fenêtre qui sera utilisée comme masque sur le signal, et dans laquelle on considère que le signal est localement stationnaire, puis on décale cette fenêtre le long du signal afin de l’analyser entièrement.
 
Figure : Transformée de Fourier fenêtrée
La transformée de Fourier fenêtrée remplace la sinusoïde de la transformée de Fourier par le produit d'une sinusoïde et d'une fenêtre localisée en temps. La définition de la STFT est donnée par la formule suivante :
 
Où : 
x(t) étant le signal lui-même 
g(t) est la fonction fenêtre 
et g^*  son complexe conjugué. 
f représente la fréquence. 
s représente l’échelle.
Comme l'indique l'équation, Pour chaque valeur de f et de s, on calcule un nouveau coefficient de la STFT. On constate que la fenêtre g est indépendante de l’échelle s, ce qui signifie que l’enveloppe de la fenêtre glissante sera constante : on aura donc une résolution fixe sur toute la durée du signal. Ainsi, l’étude d’un signal avec la STFT permet d’obtenir à la fois une information sur le temps et sur la fréquence, mais la résolution d’analyse est fixée par le choix de la taille de l’enveloppe : 
     • Si la fenêtre est trop petite, les basses fréquences n’y seront pas contenues. Si la fenêtre est trop grande, l’information sur les hautes fréquences est noyée dans l’information concernant la totalité de l’intervalle contenu dans la fenêtre. 
      Donc la taille fixe de la fenêtre est un gros inconvénient. L’outil idéal serait une fenêtre qui s’adapte aux variations de fréquence dans le signal à analyser. Cet outil existe, il s’agit de la récente analyse en ondelettes.
Transformée en ondelettes :
La transformée en ondelettes est une des solutions les plus utilisées pour surmonter les problèmes temps-fréquence de la transformée de Fourier d’une part et le problème de la taille de la fenêtre de la transformée de Fourier fenêtré d’autre part. Dans l’analyse en ondelettes, l’utilisation d’une fenêtre modulée en échelle résout le problème de découpage du signal. La fenêtre est déplacée sur le signal et pour chaque position, le spectre est calculé. Puis le processus est répété plusieurs fois avec une fenêtre légèrement plus courte (ou plus longue) pour chaque nouveau cycle : c’est l’analyse temps-échelle. A la fin, le résultat est une collection de représentations temps-fréquence du signal, à différentes résolutions. Nous parlons alors d’analyse multi-résolution. La transformation en traitement du signal. Cette transformation produit une représentation à deux paramètres (temps-échelle) d’un signal. L’échelle permet d’obtenir une nouvelle notion de caractéristique “fréquentielle” dépendant du temps. La transformée en ondelettes peut être perçue comme un intermédiaire entre la transformée de Fourier à fenêtre glissante et la transformée de Wigner Ville.
Définition d’une ondelette :
Une ondelette est une forme d'onde qui a une valeur moyenne zéro et une durée limitée. En regardant des images des ondelettes et des ondes sinusoïdales, on voit intuitivement que des signaux avec les changements pointus pourraient mieux être analysés avec une ondelette irrégulière qu'avec une sinusoïde douce.
 
Figure : La Différence entre une onde sinusoïdale et une ondelette
La transformée en ondelettes est un outil mathématique qui décompose un signal en fréquences en conservant une localisation spatiale. Le signal de départ est projeté sur un ensemble de fonctions de base qui varient en fréquence et en espace. Ces fonctions de base s’adaptent aux fréquences du signal à analyser. Cette transformation permet donc d’avoir une localisation en temps et en fréquence du signal analysé.
 
Figure : La transformée en ondelette
L'analyse en ondelettes adopte une fonction de prototype d'ondelettes connue sous le nom de "Ondelettes mère". 
 
Figure : Ondelette mère : Ondelette de Morlet
Cette Ondelette mère génère un ensemble de fonctions de base connues sous le nom " Ondelettes enfantes" par des translations et dilatations récursives. La définition de l’ondelette mère est donnée par la formule suivante :
 
 
          énergie à toutes les échelles.

Paramètre de translation :
Le sens du terme translation est celui qu'il avait dans la STFT, il est lié à la localisation de la fenêtre, à mesure que cette fenêtre est décalée sur l'étendue du signal. Ce terme correspond évidemment à une information de temps dans le domaine de la transformée. Nous n'avons pas cependant de paramètre de fréquence, comme nous l'avions avec la STFT, il est remplacé par un paramètre d'échelle défini comme 1/fréquence. Le terme fréquence reste réservé à la STFT (ou à la TF).
Paramètre d’échelle :
Le paramètre échelle, utilisé en analyse par ondelettes, est très similaire à la notion d'échelle pour les cartes. Comme dans le cas des cartes, les grandes échelles correspondent à des vues globales (du signal) non détaillées. Les faibles valeurs d'échelle correspondent à des vues détaillées. En termes de fréquence, de façon similaire, les basses fréquences (grandes échelles) fournissent une information globale sur le signal (habituellement sur tout l'étendu du signal) alors que les hautes fréquences (faibles échelles) donnent des informations détaillées sur un motif caché dans le signal (généralement de faible duré).
Type de transformée en ondelette :
On distingue deux types de transformées en ondelettes suivant que le sous-groupe Λ est discret ou continu.
Transformée en ondelettes continue CWT :
La transformée en ondelettes continue (CWT) est une représentation temps-fréquence de signaux qui présente graphiquement une similitude superficielle avec la transformée de Wigner. Une transformée en ondelettes est une convolution d'un signal s(t) avec un ensemble de fonctions qui sont générées par des translations et des dilatations d'une fonction principale. La fonction principale est appelée ondelette mère et les fonctions translatées ou dilatées sont appelées ondelettes. Mathématiquement, le CWT est donné par :
 
Ici b est la translation temporelle et a est la dilatation de l'ondelette.
D'un point de vue informatique, il est naturel d'utiliser la FFT pour calculer la convolution, ce qui suggère que les résultats dépendent d'un échantillonnage approprié de s(t). 
Lorsque l'ondelette mère est complexe, le CWT est également une fonction à valeur complexe. Sinon, le CWT est réel. L'amplitude au carré du CWT |W(a,b)|² est équivalente au spectre de puissance de sorte qu'un affichage (image) typique du CWT est une représentation du spectre de puissance en fonction du décalage temporel b. Il convient de noter cependant que la forme précise du CWT dépend du choix de l'ondelette mère y et donc l'étendue de l'équivalence entre la grandeur au carré du CWT et le spectre de puissance dépend de l'application. 
L'opération CWT est implémentée en utilisant à la fois la FFT et l'approche de la somme discrète. Vous pouvez utiliser l'un ou l'autre pour obtenir une représentation de l'ondelette effective en utilisant une fonction delta comme entrée. 

## Interfaces
   * Home page 
![image](https://user-images.githubusercontent.com/67875720/175822302-4fe290f1-0cf3-4cd3-bb44-67a5a40601a8.png)

##  Dataset used for indexing images 
![image](https://user-images.githubusercontent.com/67875720/175822424-04303663-1283-46b5-8c95-ee1f28970af4.png)

*selecting image to search 
![image](https://user-images.githubusercontent.com/67875720/175822452-72c15048-9109-41d4-b507-a6d05886b07b.png)

## Results 
![image](https://user-images.githubusercontent.com/67875720/175822465-7d59aa38-32f1-42b8-aed0-0fd7248412a4.png)

![image](https://user-images.githubusercontent.com/67875720/175822512-0f4968e7-b4fa-4922-b650-cdca8bdeb005.png)

