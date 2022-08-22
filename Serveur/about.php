<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
    <head>
        <meta charset="utf8">
        <title> Home > About</title>
        <link rel="stylesheet" href="style.css"/>

        <!-- Script pour l'ouverture de la bannière -->
        <script src="jquery.js"></script>
        <script>
            $(function(){
                $("#includedBanner").load("banner.html"); 
            });
        </script>
        <link rel="icon" href="Media\TrackSwim_logo\ts_icon.ico">
    </head>

    <body>
        <!-- Bannière -->
        <div id="includedBanner"></div>
        <center>

        <table border="0">
            <TR height="20">
                <TD width="1500" colspan="2" align="left">
                    <h2>Qu'est-ce que TrackSwim ?</h2>
                </TD>
            </TR>
            <TR height="40">
                <TD width="50" colspan="1" align="left">
                    <!-- Laisser vide pour retrait -->
                </TD>
                <TD colspan="1" align="left">
                    <strong>"TrackSwim"</strong> est le nom apporté au projet constituant le coeur du travail de Bachelor de M. Oleinikoff Alexis,<br>étudiant en dernière année à la Haute École d'Ingénierie et de Gestion du canton de Vaud (HEIG-VD), dans la fillière Microtechniques.<br><br>
                    Ce projet, ayant été proposé par l'entreprise partenaire <strong>GSInformatique SA</strong>, consiste en la réalisation d'un demonstrateur<br>sur le terrain (prototype), permettant de récolter diverses informations concernant les performances de nageurs.<br>
                    En effet, pour ce domaine sportif en particulier, il est relativement difficile de s'auto-évaluer. Les moyens existants <br> sont soit trop couteux (ex: coach privé) soit requièrent l'interruption non désirée de l'activité.<br><br>
                    Pour résoudre cette problématique, une solution a été sélectionnée. Le nageur (utilisateur) est équipé, au poignet, d'un bracelet arborant une puce <a href="https://fr.wikipedia.org/wiki/Radio-identification">RFID</a>.<br>
                    Un module contenant une antenne ainsi qu'un émetteur/récepteur détecte le départ et l'arrivée du sportif à chaque aller-retour.<br>
                    Ce dernier peut visualiser, au travers d'un afficheur 7-segments monté contre le module, son temps actuel et sa longueur totale nagée.<br> De retour chez lui, il peut aussi consulter le <a href="index.php">site officiel du projet</a>, afin d'obtenir un récapitulatif de toutes ses sessions d'entraînement.<br>
                </TD>
            </TR>
            <TR height="20">
                <TD width="1500" colspan="2" align="left">
                    <h2>Les fonctionnalités</h2>
                </TD>
            </TR>
            <TR height="40">
                <TD width="50" colspan="1" align="left">
                    <!-- Laisser vide pour retrait -->
                </TD>
                <TD colspan="1" align="left">
                    Le site est divisé en deux sections distinctes : <u>Utilisateur</u> (nageur) et <u>administrateur</u> (gestionnaire).<br>
                    <h3>→ <u>Utilisateur</u></h3>
                    L'utilisateur peut utiliser son identifiant (Nom et prénom) afin de visualiser ses performances, à la date sélectionnée.<br>
                    Ses dernières sont disponibles quelques minutes après l'arrêt de l'entraînement, tant que le bracelet <br>
                    porté au poignet a été appareilé correctement à l'utilisateur.

                    <h3>→ <u>Administrateur</u></h3>
                    L'administrateur peut gérer un certains nombre de paramètres liés à la base de données TrackSwim.<br>
                    En se connectant avec le bon identifiant, l'administrateur a directement accès à la visualisation, création, <br>
                    modification et suppresion de table dans la base de données.<br><br>
                    En cliquant sur l'œil à droite du nom de la table, il est possible de la visualiser.
                </TD>
            </TR>
            <TR height="20">
                <TD width="1500" colspan="2" align="left">
                    <h2>Les liens utiles</h2>
                </TD>
            </TR>
            <TR height="40">
                <TD width="50" colspan="1" align="left">
                    <!-- Laisser vide pour retrait -->
                </TD>
                <TD colspan="1" align="left">
                    <a href="https://www.pinterest.com/pin/swimming-moms--294915475592537220">Lien vers la source de l'image du logo</a><br><br>
                    <a href="https://www.gsinfo.ch/">Lien vers le site de <strong>GSInformatique</strong></a><br>
                    <a href="https://heig-vd.ch/">Lien vers le site de l'<strong>HEIG-VD</strong></a><br>
                    <a href="https://github.com/alexisoleinikoff/TrackSwim_Codes">Lien vers le git du projet</a><br>
                </TD>
            </TR>
        </table>
        
    </body>
<html>