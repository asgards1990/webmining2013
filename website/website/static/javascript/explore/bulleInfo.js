function chargementBulleInfo(nomDuCadre,idDuFilm,titreDuFilm){
	//if(document.getElementById("bulleInfoExt")){document.getElementById("bulleInfoExt").parentNode.removeChild(document.getElementById("bulleInfoExt"))};
	if(document.getElementById("bulleInfoExt")){
		var opts = {
			lines: 13, // The number of lines to draw
			length: 11, // The length of each line
			width: 9, // The line thickness
			radius: 29, // The radius of the inner circle
			corners: 1, // Corner roundness (0..1)
			rotate: 0, // The rotation offset
			direction: 1, // 1: clockwise, -1: counterclockwise
			color: '#000', // #rgb or #rrggbb or array of colors
			speed: 1.3, // Rounds per second
			trail: 70, // Afterglow percentage
			shadow: true, // Whether to render a shadow
			hwaccel: true, // Whether to use hardware acceleration
			className: 'spinner', // The CSS class to assign to the spinner
			zIndex: 2e9, // The z-index (defaults to 2000000000)
			top: 'auto', // Top position relative to parent in px
			left: 'auto' // Left position relative to parent in px
		};
		var target = document.getElementById('bulleInfo');
		var spinner = new Spinner(opts).spin(target);
		$.post("/cinema/filmInfo/","film_id="+idDuFilm,function(data){affecter2(data)})
		.fail(function(){
			document.getElementById('bulleInfo').removeChild(document.getElementById('bulleInfo').getElementsByClassName('spinner')[0])
			document.getElementById("conteneurTitre").textContent="Title : "+titreDuFilm;
			document.getElementById("conteneurDateSortie").textContent="Release date : ";
			document.getElementById("conteneurActeurs").textContent="Actors : ";
			document.getElementById("conteneurSynopsis").textContent="Plot : ";
		});
		function affecter2(data){
			console.log(JSON.stringify(data))
			document.getElementById('bulleInfo').removeChild(document.getElementById('bulleInfo').getElementsByClassName('spinner')[0])
			document.getElementById("conteneurTitre").textContent="Title : " + data.english_title;
			document.getElementById("conteneurDateSortie").textContent="Release date : " + data.release_date.slice(-2)+"/"+data.release_date.slice(-5,-3)+"/"+data.release_date.slice(0,4);
			var stringActors="Actors : ";
			for(var i=0; i<data.actors.length;i++){
				stringActors=stringActors+data.actors[i].name;
				if(i!=data.actors.length-1){
					stringActors=stringActors+", ";
				}
			}
			document.getElementById("conteneurActeurs").textContent=stringActors;
			document.getElementById("conteneurSynopsis").textContent="Plot : " + data.plot;
		}		
	}
	else{
		var bulleInfoExt=document.createElement("div");
		bulleInfoExt.id="bulleInfoExt";
		document.getElementById(nomDuCadre).appendChild(bulleInfoExt);
		bulleInfoExt.style.cssText="width:100%; height:100%; display: none;"	
		var bulleInfo=document.createElement("div");
		bulleInfo.id="bulleInfo";
		bulleInfo.style.cssText="border:1px Grey solid"
		document.getElementById("bulleInfoExt").appendChild(bulleInfo);
		var TitreInfo=document.createElement("h1");
		TitreInfo.id="TitreInfo";
		document.getElementById("bulleInfo").appendChild(TitreInfo);
		var conteneurInfo=document.createElement('p');
		conteneurInfo.id="conteneurInfo";
		document.getElementById("bulleInfo").appendChild(conteneurInfo);
		
		$.post("/cinema/filmInfo/","film_id="+idDuFilm,function(data){affecter(data)});
		
		function affecter(data){
			console.log(JSON.stringify(data))
			var conteneurTitre=document.createElement('p');
			conteneurTitre.id="conteneurTitre";
			conteneurTitre.style.cssText='margin-left:2px; margin-right:2px; margin-top:4px; margin-bottom:0px;float:left;width:100%;text-align: left;'
			TitreInfo.appendChild(conteneurTitre)
			var conteneurDateSortie=document.createElement('p');
			conteneurDateSortie.id="conteneurDateSortie";
			conteneurDateSortie.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: left;'
			TitreInfo.appendChild(conteneurDateSortie)
			var conteneurRealisateur=document.createElement('p');
			conteneurRealisateur.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: left;'
			conteneurInfo.appendChild(conteneurRealisateur)
			var conteneurActeurs=document.createElement('p');
			conteneurActeurs.id="conteneurActeurs";
			conteneurActeurs.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: left;'
			conteneurInfo.appendChild(conteneurActeurs)
			var conteneurSynopsis=document.createElement('p');
			conteneurSynopsis.id="conteneurSynopsis";
			conteneurSynopsis.style.cssText='margin-left:2px; margin-right:2px;margin-top:12px;margin-bottom:0px;float:left;width:100%;text-align: left;'
			conteneurInfo.appendChild(conteneurSynopsis)
			var texteTitre=document.createTextNode("Title : " + data.english_title);
			conteneurTitre.appendChild(texteTitre)
			var texteDateSortie=document.createTextNode("Release date : " + data.release_date.slice(-2)+"/"+data.release_date.slice(-5,-3)+"/"+data.release_date.slice(0,4));
			conteneurDateSortie.appendChild(texteDateSortie)
			/*var texteRealisateur=document.createTextNode("Director : " + data.release_date);
			conteneurRealisateur.appendChild(texteRealisateur)*/
			var texteActeurs=document.createTextNode("");
			var stringActors="Actors : ";
			for(var i=0; i<data.actors.length;i++){
				stringActors=stringActors+data.actors[i].name;
				if(i!=data.actors.length-1){
					stringActors=stringActors+", ";
				}
			}
			conteneurActeurs.appendChild(texteActeurs)
			texteActeurs.textContent=stringActors;
			var texteSynopsis=document.createTextNode("Plot : " + data.plot);
			//var conteneurSynopsis=document.createElement('p');
			
			conteneurSynopsis.appendChild(texteSynopsis)
			//$("#bulleInfoExt").fadeIn(1000);
			$("#bulleInfoExt").fadeIn(1000);
		}
	}
}

