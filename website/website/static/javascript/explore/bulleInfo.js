function chargementBulleInfo(nomDuCadre,idDuFilm){
	//if(document.getElementById("bulleInfoExt")){document.getElementById("bulleInfoExt").parentNode.removeChild(document.getElementById("bulleInfoExt"))};
	if(document.getElementById("bulleInfoExt")){
		document.getElementById("conteneurTitre").textContent="Title : ";
		document.getElementById("conteneurDateSortie").textContent="Release date : ";
		document.getElementById("conteneurActeurs").textContent="Actors : ";
		document.getElementById("conteneurSynopsis").textContent="Plot : ";
		$.post("/cinema/filmInfo/","film_id="+idDuFilm,function(data){affecter2(data)});
		function affecter2(data){
			console.log(JSON.stringify(data))
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
			conteneurSynopsis.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: justify;'
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

