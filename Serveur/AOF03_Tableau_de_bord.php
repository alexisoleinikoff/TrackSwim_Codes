<!doctype html>
<html>
	<head>
		<title>Première application projet swimtrack</title>    
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		
		<script language="javascript">
			//A mettre ici les scripts
		</script>
		 
	</head>
	<body scroll="no">	
	   	<H1>Premier tableau de bord Swimtrack!</H1>
		<table align="center"  border="1">
			<TR height="50">
				<TD width="500"  colspan="2" align="center">
					Première étape : On va juste lire la liste des personnes
				</TD>
			</TR>
			<TR>
				<form name="maforme1"  action="lister_personnes.php" method="POST">
					<TD width="300">
						En cliquant sur ce bouton on lira les personnes inscrites dans la BD swimtrack
					</TD>
					<TD width="200">
						<input type="submit" value="lister les personnes de la BD" />
					</TD>
				</form>
			</TR>
		</table>
	</body>
</html>