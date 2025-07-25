<h1>Projet IOT python</h1>

<h3>Comment démarrer le projet<h3>
<ul>
    <li>1. pour lancer le projet sans trop de soucis, tout d'abord faut lancer la bdd mysql et importer la bdd depuis le dossier '/bdd' (les données basiques de test sont dedans, si vous voulez des données fraiches faut les supprimer)</li>
    <li>2. lancer le broker mqtt sur HiveMQ -> "https://www.hivemq.com/demos/websocket-client/" et ajouter deux topic subscription ('kstest/#' et 'arrosage/control')</li>
    <li>3. lancer le reste des scripts: le subscriber -> python ./subscriber3.py</li>
    <li>4. lancer le streamlit: python -m streamlit run ./streamlit.py (seulement si 'streamlit run ./streamlit.py' ne marche pas pour X raison)</li>
    <li>5. lancer le projet wokwi: https://wokwi.com/projects/437394984925335553 ou copier le code depuis le ficher /main.py et le diagram.json dans le dossier /wokwi</li>
</ul>