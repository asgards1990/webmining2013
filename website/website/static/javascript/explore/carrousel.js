var carrouselDispo;


function carrousel(nomDuCadre,data){
	//alert("hello")
	var tableauId=new Array;
	var repLien=new Array;
	//alert(data.nbresults)
	var nombre = data.nbresults;
	//alert(nombre);
	var ontTousRep=new Array;
	for (var i=0;i < nombre;i++){
		ontTousRep[5+((1-2*(i%2))*(Math.floor(i/2)+1))]=0;
	}
	for (var i=0;i < nombre;i++){
		tableauId[5+((1-2*(i%2))*(Math.floor(i/2)+1))]=data.results[i].id;		//remplacer 0 par i
		//Bloc à changer quand on peut récupérer les infos sur notre propre serv
		function encap(i,data,nombre){
			return function(data){
				repLien[5+((1-2*(i%2))*(Math.floor(i/2)+1))]=eval("(" + data + ")").Poster;
				ontTousRep[5+((1-2*(i%2))*(Math.floor(i/2)+1))]=1;
				var mult=1;
				for(var j=0; j<nombre;j++){
					mult=mult*ontTousRep[5+((1-2*(j%2))*(Math.floor(j/2)+1))];
				}
				if (mult==1) {
					repLien[5]="../pesto/static/img/explore/film1.jpg";
					for(var j=nombre;j<10;j++){
						repLien[5+((1-2*(j%2))*(Math.floor(j/2)+1))]="../pesto/static/img/explore/filmVide.jpg";
					}
					carrousel2(nomDuCadre,repLien)
				}
			}
		}
		$.get("http://www.omdbapi.com/?i=" + tableauId[5+((1-2*(i%2))*(Math.floor(i/2)+1))], encap(i,data,nombre))
	}
}

function carrousel2(nomDuCadre,lienImage){
	//alert(lienImage)
	var largeur=75;//1*contenu.width;
	var hauteur=100;//1*contenu.height;
	var imageLoaded=new Array;
	var coeffLargeur=new Array;
	var coeffHauteur=new Array;
	for(var l=0; l <11;l++){imageLoaded[l]=false;}
	carrouselDispo=false;
	var imageinter=new Array;
	for(var l=0; l <11;l++){
		imageinter[l]=new Image();
		imageinter[l].src = lienImage[l];//"film"+(l+1)+".jpg";
		//coeffLargeur[l]=75/imageinter[l].width;
		//coeffHauteur[l]=100/imageinter[l].height;
		imageinter[l].onload = scopeChargement(l);
	}
	function scopeChargement(l){return function(){coeffLargeur[l]=75/imageinter[l].width;coeffHauteur[l]=100/imageinter[l].height;imageLoaded[l]=true; toutEstCharge()}}

	function toutEstCharge(){
		//alert(imageLoaded)
		if(imageLoaded[0]==true && imageLoaded[1]==true && imageLoaded[2]==true && imageLoaded[3]==true && imageLoaded[4]==true && imageLoaded[5]==true && imageLoaded[6]==true && imageLoaded[7]==true && imageLoaded[8]==true && imageLoaded[9]==true && imageLoaded[10]==true){
			//alert("!!!!!!!")
			actionAFaire();
		}
	}

	function actionAFaire() {

	//var contenu = new Image();
	//contenu.src= "film1.jpg";
	//var largeur=75;//1*contenu.width;
	//var hauteur=100;//1*contenu.height;
	//alert(largeur + " " + hauteur)
	
	var listCanvas;


	for(var i=0; i <11;i++){
		canv = document.createElement('canvas');
		canv.id = 'canv'+(i+1);
		canv.setAttribute("width", largeur);
		canv.setAttribute("height", hauteur);
		if(i<=5){
			canv.style.cssText ='position:absolute;display:none;top:0px;left:'+i*largeur/2+'px;z-index:'+i+';';
		}
		else{
			canv.style.cssText ='position:absolute;display:none;top:0px;left:'+i*largeur/2+'px;z-index:'+(10-i)+';';
		}		
		document.getElementById(nomDuCadre).appendChild(canv);
	}

	var coeffAffiche = new Array;
	coeffAffiche[1]=[0.6,0.2,0,0.98,0,0];
	coeffAffiche[2]=[0.65,0.2,0,0.98,0,0];
	coeffAffiche[3]=[0.7,0.2,0,0.98,0,0];
	coeffAffiche[4]=[0.75,0.2,0,0.98,0,0];
	coeffAffiche[5]=[0.8,0.2,0,0.98,0,0];
	coeffAffiche[6]=[1,0,0,1,0,0];
	coeffAffiche[7]=[0.8,-0.2,0,0.96*hauteur/(hauteur+0.2*largeur), 0.2*largeur, 0.1*largeur];
	coeffAffiche[8]=[0.75,-0.2,0,0.96*hauteur/(hauteur+0.2*largeur), 0.2*largeur, 0.1*largeur];
	coeffAffiche[9]=[0.7,-0.2,0,0.96*hauteur/(hauteur+0.2*largeur), 0.2*largeur, 0.1*largeur];
	coeffAffiche[10]=[0.65,-0.2,0,0.96*hauteur/(hauteur+0.2*largeur), 0.2*largeur, 0.1*largeur];
	coeffAffiche[11]=[0.6,-0.2,0,0.96*hauteur/(hauteur+0.2*largeur), 0.2*largeur, 0.1*largeur];

	function encapsuler(h){
		return function(){dessiner(h);};
	}
	
	//var image=new Array;
	function dessiner(h){
		//image[h]=new Image();
		//image[h].src = "film"+(h+1)+".jpg";
		//image[h].onload = function() {
        		var width = imageinter[h].width,
            		height = imageinter[h].height;
        		var context = $("#canv"+(h+1))[0].getContext("2d");
        		for (var i = 0; i <= height / 2; ++i) {
            			context.setTransform(coeffLargeur[h]*coeffAffiche[h+1][0], coeffHauteur[h]*coeffAffiche[h+1][1]*i/height,coeffLargeur[h]*coeffAffiche[h+1][2], coeffHauteur[h]*coeffAffiche[h+1][3], coeffAffiche[h+1][4], coeffAffiche[h+1][5]);
            			context.drawImage(imageinter[h], 0, height/2-i, width, 2, 0, height/2-i, width, 2);
            			context.setTransform(coeffLargeur[h]*coeffAffiche[h+1][0], -coeffHauteur[h]*coeffAffiche[h+1][1]*i/height,-coeffLargeur[h]*coeffAffiche[h+1][2], coeffHauteur[h]*coeffAffiche[h+1][3], coeffAffiche[h+1][4], coeffAffiche[h+1][5]);
            			context.drawImage(imageinter[h],0, height/2+i, width, 2, 0, height/2+i, width, 2);
        		}
    		//};
    		//image.src = "film"+(h+1)+".jpg";		
	}

	for (var j = 0; j < 11; j++) {
		dessiner(j);
	}
	
	var fadeTime=1000;
	var fadeIntervalle=100;
	$("#canv6").fadeIn(fadeTime)
	setTimeout(function(){$("#canv5").fadeIn(fadeTime),$("#canv7").fadeIn(fadeTime)},fadeIntervalle)
	setTimeout(function(){$("#canv4").fadeIn(fadeTime),$("#canv8").fadeIn(fadeTime)},2*fadeIntervalle)
	setTimeout(function(){$("#canv3").fadeIn(fadeTime),$("#canv9").fadeIn(fadeTime)},3*fadeIntervalle)
	setTimeout(function(){$("#canv2").fadeIn(fadeTime),$("#canv10").fadeIn(fadeTime)},4*fadeIntervalle)
	setTimeout(function(){$("#canv1").fadeIn(fadeTime),$("#canv11").fadeIn(fadeTime,function(){carrouselDispo=true;})},5*fadeIntervalle)


	var positioninv = new Array;
	for (var j = 1; j <= 11; j++) {
		positioninv[j]="canv"+j;
	}

	function transitionUnCoup(etape,nombreDePas,numeroAffiche,pos,direction){	
		var arrivee;	
		var depart=numeroAffiche;		
		if(direction=="droite"){
			arrivee=(numeroAffiche)%11+1;
		}
		else{
			arrivee=(numeroAffiche+9)%11+1;
		}
		var image=new Image();
		//image.src=imageinter[pos.slice(4)-1].src;
		image=imageinter[pos.slice(4)-1];
		//alert(coeffLargeur[0])
		//alert(pos.slice(4)-1)
		//image.src="film1.jpg";
		var width=image.width;
		var height=image.height;
		var context = $("#"+pos)[0].getContext("2d");
		context.clearRect(0, 0, largeur, hauteur);
		var canvas = document.getElementById(pos);
		var w=canvas.width;		
		canvas.width = 1;
  		canvas.width = w;
        	for (var i = 0; i <= height / 2; ++i) {
            		context.setTransform((coeffAffiche[depart][0]+(coeffAffiche[arrivee][0]-coeffAffiche[depart][0])*etape/nombreDePas)*coeffLargeur[pos.slice(4)-1],
				((coeffAffiche[depart][1]+(coeffAffiche[arrivee][1]-coeffAffiche[depart][1])*etape/nombreDePas) * i / height)*coeffHauteur[pos.slice(4)-1],
				(coeffAffiche[depart][2]+(coeffAffiche[arrivee][2]-coeffAffiche[depart][2])*etape/nombreDePas)*coeffLargeur[pos.slice(4)-1],
				(coeffAffiche[depart][3]+(coeffAffiche[arrivee][3]-coeffAffiche[depart][3])*etape/nombreDePas)*coeffHauteur[pos.slice(4)-1],
				coeffAffiche[depart][4]+(coeffAffiche[arrivee][4]-coeffAffiche[depart][4])*etape/nombreDePas,
				coeffAffiche[depart][5]+(coeffAffiche[arrivee][5]-coeffAffiche[depart][5])*etape/nombreDePas);
            		context.drawImage(image, 0, height / 2 - i, width, 2, 0, height / 2 - i, width, 2);
            		context.setTransform((coeffAffiche[depart][0]+(coeffAffiche[arrivee][0]-coeffAffiche[depart][0])*etape/nombreDePas)*coeffLargeur[pos.slice(4)-1],
				(-(coeffAffiche[depart][1]+(coeffAffiche[arrivee][1]-coeffAffiche[depart][1])*etape/nombreDePas) * i / height)*coeffHauteur[pos.slice(4)-1],
				(coeffAffiche[depart][2]+(coeffAffiche[arrivee][2]-coeffAffiche[depart][2])*etape/nombreDePas)*coeffLargeur[pos.slice(4)-1],
				(coeffAffiche[depart][3]+(coeffAffiche[arrivee][3]-coeffAffiche[depart][3])*etape/nombreDePas)*coeffHauteur[pos.slice(4)-1],
				coeffAffiche[depart][4]+(coeffAffiche[arrivee][4]-coeffAffiche[depart][4])*etape/nombreDePas,
				coeffAffiche[depart][5]+(coeffAffiche[arrivee][5]-coeffAffiche[depart][5])*etape/nombreDePas);
            		context.drawImage(image, 0, height / 2 + i, width, 2, 0, height / 2 + i, width, 2);
        	}
	}


	
	function toutUnCoup(etape,nbDePas,direction,pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,pos9,pos10,pos11){
		return function(){
			transitionUnCoup(etape,nbDePas,1,pos1,direction);
			transitionUnCoup(etape,nbDePas,2,pos2,direction);
			transitionUnCoup(etape,nbDePas,3,pos3,direction);
			transitionUnCoup(etape,nbDePas,4,pos4,direction);
			transitionUnCoup(etape,nbDePas,5,pos5,direction);
			transitionUnCoup(etape,nbDePas,6,pos6,direction);
			transitionUnCoup(etape,nbDePas,7,pos7,direction);
			transitionUnCoup(etape,nbDePas,8,pos8,direction);
			transitionUnCoup(etape,nbDePas,9,pos9,direction);
			transitionUnCoup(etape,nbDePas,10,pos10,direction);
			transitionUnCoup(etape,nbDePas,11,pos11,direction);
			if(etape<nbDePas/2){
				for(var i=0; i <11;i++){
					switch(i){
						case 0:	document.getElementById(pos1).style.zIndex=i; break;
						case 1:	document.getElementById(pos2).style.zIndex=i; break;
						case 2:	document.getElementById(pos3).style.zIndex=i; break;
						case 3:	document.getElementById(pos4).style.zIndex=i; break;
						case 4:	document.getElementById(pos5).style.zIndex=i; break;
						case 5:	document.getElementById(pos6).style.zIndex=i; break;
						case 6: document.getElementById(pos7).style.zIndex=(10-i); break;
						case 7:	document.getElementById(pos8).style.zIndex=(10-i); break;
						case 8:	document.getElementById(pos9).style.zIndex=(10-i); break;
						case 9:	document.getElementById(pos10).style.zIndex=(10-i); break;
						case 10: document.getElementById(pos11).style.zIndex=(10-i); break;
					}
					/*if(i<=5){
						document.getElementById(positioninv[i+1]).style.zIndex=i;
					}
					else{
						document.getElementById(positioninv[i+1]).style.zIndex=(10-i);
					}*/
				}
			}
			else{
				if (direction=="droite"){
					for(var i=0; i <11;i++){
						switch(i){
							case 0:	document.getElementById(pos1).style.zIndex=i+1; break;
							case 1:	document.getElementById(pos2).style.zIndex=i+1; break;
							case 2:	document.getElementById(pos3).style.zIndex=i+1; break;
							case 3:	document.getElementById(pos4).style.zIndex=i+1; break;
							case 4:	document.getElementById(pos5).style.zIndex=i+1; break;
							case 5:	document.getElementById(pos6).style.zIndex=(9-i); break;
							case 6: document.getElementById(pos7).style.zIndex=(9-i); break;
							case 7:	document.getElementById(pos8).style.zIndex=(9-i); break;
							case 8:	document.getElementById(pos9).style.zIndex=(9-i); break;
							case 9:	document.getElementById(pos10).style.zIndex=(9-i); break;
							case 10: document.getElementById(pos11).style.zIndex=0; break;
						}
					
						/*if(i<=4){
							document.getElementById(positioninv[i+1]).style.zIndex=i+1;
						}
						else{
							if(i!==10){document.getElementById(positioninv[i+1]).style.zIndex=(9-i);}
							else{document.getElementById(positioninv[i+1]).style.zIndex=0}
						}*/
					}
					
				}
				else{
					for(var i=0; i <11;i++){
						switch(i){
							case 0:	document.getElementById(pos1).style.zIndex=0; break;
							case 1:	document.getElementById(pos2).style.zIndex=i-1; break;
							case 2:	document.getElementById(pos3).style.zIndex=i-1; break;
							case 3:	document.getElementById(pos4).style.zIndex=i-1; break;
							case 4:	document.getElementById(pos5).style.zIndex=i-1; break;
							case 5:	document.getElementById(pos6).style.zIndex=i-1; break;
							case 6: document.getElementById(pos7).style.zIndex=i-1; break;
							case 7:	document.getElementById(pos8).style.zIndex=(11-i); break;
							case 8:	document.getElementById(pos9).style.zIndex=(11-i); break;
							case 9:	document.getElementById(pos10).style.zIndex=(11-i); break;
							case 10: document.getElementById(pos11).style.zIndex=(11-i); break;
						}
						/*if(i<=6){
							if(i!==0){document.getElementById(positioninv[i+1]).style.zIndex=i-1;}
							else{document.getElementById(positioninv[i+1]).style.zIndex=0;}
						}
						else{
							document.getElementById(positioninv[i+1]).style.zIndex=(11-i);
						}*/
					}
				}
			}
		}
	}

	var enCours=false
	var inter=new Array;
	var inter2;
	function decalerUnCranDroite(nombreDePas,multiVit,relacher){
		var nbDecal=1;
		$('#'+positioninv[1]).animate({left:((nbDecal+0)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[2]).animate({left:((nbDecal+1)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[3]).animate({left:((nbDecal+2)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[4]).animate({left:((nbDecal+3)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[5]).animate({left:((nbDecal+4)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[6]).animate({left:((nbDecal+5)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[7]).animate({left:((nbDecal+6)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[8]).animate({left:((nbDecal+7)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[9]).animate({left:((nbDecal+8)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[10]).animate({left:((nbDecal+9)%11)*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[11]).animate({left:((nbDecal+10)%11)*largeur/2+'px'},400/multiVit);
		for (var i=1;i<nombreDePas+1;i++){
			setTimeout(toutUnCoup(i,nombreDePas,"droite",positioninv[1],positioninv[2],positioninv[3],positioninv[4],positioninv[5],positioninv[6],positioninv[7],positioninv[8],positioninv[9],positioninv[10],positioninv[11]),i*(400/multiVit)/nombreDePas);
		}
		//setTimeout(function(){
			for (var j=1;j<12;j++){
				inter[j]=positioninv[j];
			}
			for (var k=1;k<12;k++){
				positioninv[k]=inter[(k+9)%11+1];
			}
			if (relacher==true){enCours=false;}
			//},400/multiVit+10)
	}

	function decalerUnCranGauche(nombreDePas,multiVit,relacher){
		$('#'+positioninv[1]).animate({left:10*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[2]).animate({left:'0px'},400/multiVit);
		$('#'+positioninv[3]).animate({left:largeur/2+'px'},400/multiVit);
		$('#'+positioninv[4]).animate({left:2*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[5]).animate({left:3*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[6]).animate({left:4*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[7]).animate({left:5*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[8]).animate({left:6*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[9]).animate({left:7*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[10]).animate({left:8*largeur/2+'px'},400/multiVit);
		$('#'+positioninv[11]).animate({left:9*largeur/2+'px'},400/multiVit);
		for (var i=1;i<nombreDePas+1;i++){
			setTimeout(toutUnCoup(i,nombreDePas,"gauche",positioninv[1],positioninv[2],positioninv[3],positioninv[4],positioninv[5],positioninv[6],positioninv[7],positioninv[8],positioninv[9],positioninv[10],positioninv[11]),i*(400/multiVit)/nombreDePas);
		}
		//setTimeout(function(){
		inter2=positioninv[1];
		positioninv[1]=positioninv[2];
		positioninv[2]=positioninv[3];
		positioninv[3]=positioninv[4];
		positioninv[4]=positioninv[5];
		positioninv[5]=positioninv[6];
		positioninv[6]=positioninv[7];
		positioninv[7]=positioninv[8];
		positioninv[8]=positioninv[9];
		positioninv[9]=positioninv[10];
		positioninv[10]=positioninv[11];
		positioninv[11]=inter2;
		if (relacher==true){enCours=false;}
		//},400/multiVit+10)
	}
	//for (var i=1;i<12;i++){
	function defClic(entier){
		if(enCours===false){
			enCours=true;
			var position=positioninv.indexOf("canv"+entier);
			switch(position){
				case 1:
					decalerUnCranDroite(3,2,false)
					setTimeout(function(){decalerUnCranDroite(3,2,false)},400/2)//+50)
					setTimeout(function(){decalerUnCranDroite(3,2,false)},2*400/2)//+2*50)
					setTimeout(function(){decalerUnCranDroite(3,2,false)},3*400/2)//+3*50)
					setTimeout(function(){decalerUnCranDroite(3,2,true)},4*400/2)//+4*50)
					break;
				case 2:
					decalerUnCranDroite(3,2,false)
					setTimeout(function(){decalerUnCranDroite(3,2,false)},400/2)//+50)
					setTimeout(function(){decalerUnCranDroite(3,2,false)},2*400/2)//+2*50)
					setTimeout(function(){decalerUnCranDroite(3,2,true)},3*400/2)//+3*50)
					break;
				case 3:
					decalerUnCranDroite(3,2,false)
					setTimeout(function(){decalerUnCranDroite(3,2,false)},400/2)//+50)
					setTimeout(function(){decalerUnCranDroite(3,2,true)},2*400/2)//+2*50)
					break;
				case 4:
					decalerUnCranDroite(3,1.5,false)
					setTimeout(function(){decalerUnCranDroite(3,1.5,true)},400/1.5)//+50)
					break;
				case 5:
					decalerUnCranDroite(3,1,true)
					break;
				case 6:
					enCours=false;
					break;
				case 7:
					decalerUnCranGauche(3,1,true)
					break;
				case 8:
					decalerUnCranGauche(3,1.5,false)
					setTimeout(function(){decalerUnCranGauche(3,1.5,true)},400/1.5)//+50)
					break;
				case 9:
					decalerUnCranGauche(3,2,false)
					setTimeout(function(){decalerUnCranGauche(3,2,false)},400/2)//+50)
					setTimeout(function(){decalerUnCranGauche(3,2,true)},2*400/2)//+2*50)
					break;
				case 10:
					decalerUnCranGauche(3,2,false)
					setTimeout(function(){decalerUnCranGauche(3,2,false)},400/2)//+50)
					setTimeout(function(){decalerUnCranGauche(3,2,false)},2*400/2)//+2*50)
					setTimeout(function(){decalerUnCranGauche(3,2,true)},3*400/2)//+3*50)
					break;
				case 11:
					decalerUnCranGauche(3,2,false)
					setTimeout(function(){decalerUnCranGauche(3,2,false)},400/2)//+50)
					setTimeout(function(){decalerUnCranGauche(3,2,false)},2*400/2)//+2*50)
					setTimeout(function(){decalerUnCranGauche(3,2,false)},3*400/2)//+3*50)
					setTimeout(function(){decalerUnCranGauche(3,2,true)},4*400/2)//+4*50)
					break;
			}
		}	
	}


	$("#canv1").click(function(){if(carrouselDispo==true && imageinter[0].src.slice(-12) != "filmVide.jpg"){
		//alert(imageinter[0].src.slice(-12))
		defClic(1);chargementBulleInfo("cadreInfo","Film 1");}
	});
	$("#canv2").click(function(){if(carrouselDispo==true && imageinter[1].src.slice(-12) != "filmVide.jpg"){
		defClic(2);chargementBulleInfo("cadreInfo","Film 2");}
	});
	$("#canv3").click(function(){if(carrouselDispo==true && imageinter[2].src.slice(-12) != "filmVide.jpg"){
		defClic(3);chargementBulleInfo("cadreInfo","Film 3");}
	});
	$("#canv4").click(function(){if(carrouselDispo==true && imageinter[3].src.slice(-12) != "filmVide.jpg"){
		defClic(4);chargementBulleInfo("cadreInfo","Film 4");}
	});
	$("#canv5").click(function(){if(carrouselDispo==true && imageinter[4].src.slice(-12) != "filmVide.jpg"){
		defClic(5);chargementBulleInfo("cadreInfo","Film 5");}
	});
	$("#canv6").click(function(){if(carrouselDispo==true && imageinter[5].src.slice(-12) != "filmVide.jpg"){
		defClic(6);chargementBulleInfo("cadreInfo","Film 6");}
	});
	$("#canv7").click(function(){if(carrouselDispo==true && imageinter[6].src.slice(-12) != "filmVide.jpg"){
		defClic(7);chargementBulleInfo("cadreInfo","Film 7");}
	});
	$("#canv8").click(function(){if(carrouselDispo==true && imageinter[7].src.slice(-12) != "filmVide.jpg"){
		defClic(8);chargementBulleInfo("cadreInfo","Film 8");}
	});
	$("#canv9").click(function(){if(carrouselDispo==true && imageinter[8].src.slice(-12) != "filmVide.jpg"){
		defClic(9);chargementBulleInfo("cadreInfo","Film 9");}
	});
	$("#canv10").click(function(){if(carrouselDispo==true && imageinter[9].src.slice(-12) != "filmVide.jpg"){
		defClic(10);chargementBulleInfo("cadreInfo","Film 10");}
	});
	$("#canv11").click(function(){if(carrouselDispo==true && imageinter[10].src.slice(-12) != "filmVide.jpg"){
		defClic(11);chargementBulleInfo("cadreInfo","Film 11");}
	});
	
	}
	
}
