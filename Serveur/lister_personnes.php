<html>
	<head>
		<title>Afficher les personnes</title>    
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	</head>
	
	<body>
		<div>

			<!-- Connexion à la base de données -->
			<?php
				include 'path_BD.php';
				try
				{
					$bdd = new PDO($mon_Path_BD, $mon_userName, $monPSW);
					echo "BD ouverte <BR>";
				}
				catch (Exception $e)
				{
					die('Erreur : ' . $e->getMessage());
				}
			
			?>
			<p> un peu de html ... au cas où <p>
		
			<?php		
				// création et exécution de la requête
				$lesPersonnes = $bdd->query('SELECT * FROM user');
				
				// création de la structure d'accueil HTML
				echo '</BR>';
				echo '<h3 align="center" class="bordered"> liste des personnes </h3>
						<table align="center" border="1">
							<TR>
								<TH width="150">Nom</TH>
								<TH width="150">Prénom</TH>
								<TH width="100">Date de naissance</TH>
							</TR>';
							
				// extraction depuis la requête de la liste des personnes et remplissage de la table			
				foreach ($lesPersonnes as $unePersonne) {
					echo '<TR>
								<TD>' .$unePersonne['Nom']. '</TD> <TD>' .$unePersonne['Prénom']. '</TD> <TD>' .$unePersonne['Date de naissance'].'</TD>						
						  </TR>';
				}
				echo '</table>';
			?>
			<a href="AOF03_Tableau_de_bord.php">retour à la page principale</a>
		</div>
	</body>
</html>