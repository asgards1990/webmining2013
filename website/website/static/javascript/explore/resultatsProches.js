var coeffDist=new Array;
for(i=0;i<10;i++){coeffDist[i]=Math.ceil(100*Math.random())/100}

var numeroLigne=new Array;
var placeSurLaLigne=new Array;
var rajoutAngle=new Array;

function coeffSort(tableau){
	var sortedArray=new Array;
	for (var i = 0;i<tableau.length;i++){
		sortedArray[i]=-1;
	}
	for (var i = 0;i<tableau.length;i++){
		for (var j = 0;j<tableau.length;j++){
			dejaPris=false;
			for (var k = 0;k<tableau.length;k++){
				if(sortedArray[k]==j){dejaPris=true;}
			}
			if (dejaPris==false){
				if(sortedArray[i]==-1){
					sortedArray[i]=j;
				}
				else{
					if(tableau[j]<tableau[sortedArray[i]]){sortedArray[i]=j;}
				}
			}
		}
	}
	return sortedArray;
}

var coeffTailleCadreTitre=0.2;

function longueurEtAngle(coeffDist,largeurBox,hauteurBox,coeffEmToPx){
	var largeurCadreTitre=coeffTailleCadreTitre*largeurBox;
	var dist0EnPx=coeffEmToPx*3+largeurCadreTitre/2;
	var dist1EnPx=Math.sqrt((dist0EnPx)*(dist0EnPx)+(coeffEmToPx*2)*(coeffEmToPx*2));
	var dist2EnPx=Math.sqrt((largeurCadreTitre/2)*(largeurCadreTitre/2)+(coeffEmToPx*4)*(coeffEmToPx*4));
	var dist3EnPx=Math.sqrt((largeurCadreTitre/2)*(largeurCadreTitre/2)+(coeffEmToPx*6)*(coeffEmToPx*6));
	var dist4EnPx=Math.sqrt((largeurCadreTitre/2)*(largeurCadreTitre/2)+(coeffEmToPx*8)*(coeffEmToPx*8));
	var distMin=Math.max(dist0EnPx,dist1EnPx,dist2EnPx);
	var margeDroite=10;
	
	var coeffTrie=coeffSort(coeffDist);
	var distMaxLigne0=largeurBox/2-margeDroite-largeurCadreTitre/2;
	var distMaxLigne1=Math.sqrt(distMaxLigne0*distMaxLigne0+(coeffEmToPx*2)*(coeffEmToPx*2));
	var distMaxLigne2=Math.sqrt(distMaxLigne0*distMaxLigne0+(coeffEmToPx*4)*(coeffEmToPx*4));
	var distMaxLigne3=Math.sqrt(distMaxLigne0*distMaxLigne0+(coeffEmToPx*6)*(coeffEmToPx*6));
	var distMaxLigne4=Math.sqrt(distMaxLigne0*distMaxLigne0+(coeffEmToPx*8)*(coeffEmToPx*8));
		
	var distHyp0=new Array; var distHyp1=new Array; var distHyp2=new Array; var distHyp3=new Array; var distHyp4=new Array;
	for (var i=0;i<10;i++){
		distHyp0[i]=distMin+coeffDist[i]*(distMaxLigne0-distMin);
		distHyp1[i]=distMin+coeffDist[i]*(distMaxLigne1-distMin);
		distHyp2[i]=distMin+coeffDist[i]*(distMaxLigne2-distMin);
		distHyp3[i]=distMin+coeffDist[i]*(distMaxLigne3-distMin);
		distHyp4[i]=distMin+coeffDist[i]*(distMaxLigne4-distMin);
	}
	
	var hyp0=true; var hyp1=true; var hyp2=true; var hyp3=true; var hyp4=true; 
	if(distHyp0[coeffTrie[0]]>distMaxLigne0){hyp0=false;}
	if(distHyp0[coeffTrie[1]]>distMaxLigne0){hyp0=false;}
	if(distHyp0[coeffTrie[2]]>distMaxLigne3){hyp0=false;}
	if(distHyp0[coeffTrie[3]]>distMaxLigne3){hyp0=false;}
	if(distHyp0[coeffTrie[4]]>distMaxLigne3){hyp0=false;}
	if(distHyp0[coeffTrie[5]]>distMaxLigne3){hyp0=false;}
	if(distHyp0[coeffTrie[6]]>distMaxLigne4){hyp0=false;}
	if(distHyp0[coeffTrie[7]]>distMaxLigne4){hyp0=false;}
	if(distHyp0[coeffTrie[8]]>distMaxLigne4){hyp0=false;}
	if(distHyp0[coeffTrie[9]]>distMaxLigne4){hyp0=false;}
	
	if(distHyp1[coeffTrie[0]]>distMaxLigne0){hyp1=false;}
	if(distHyp1[coeffTrie[1]]>distMaxLigne0){hyp1=false;}
	if(distHyp1[coeffTrie[2]]>distMaxLigne3){hyp1=false;}
	if(distHyp1[coeffTrie[3]]>distMaxLigne3){hyp1=false;}
	if(distHyp1[coeffTrie[4]]>distMaxLigne3){hyp1=false;}
	if(distHyp1[coeffTrie[5]]>distMaxLigne3){hyp1=false;}
	if(distHyp1[coeffTrie[6]]>distMaxLigne4){hyp1=false;}
	if(distHyp1[coeffTrie[7]]>distMaxLigne4){hyp1=false;}
	if(distHyp1[coeffTrie[8]]>distMaxLigne4){hyp1=false;}
	if(distHyp1[coeffTrie[9]]>distMaxLigne4){hyp1=false;}
	
	if(distHyp2[coeffTrie[0]]>distMaxLigne0){hyp2=false;}
	if(distHyp2[coeffTrie[1]]>distMaxLigne0){hyp2=false;}
	if(distHyp2[coeffTrie[2]]>distMaxLigne3){hyp2=false;}
	if(distHyp2[coeffTrie[3]]>distMaxLigne3){hyp2=false;}
	if(distHyp2[coeffTrie[4]]>distMaxLigne3){hyp2=false;}
	if(distHyp2[coeffTrie[5]]>distMaxLigne3){hyp2=false;}
	if(distHyp2[coeffTrie[6]]>distMaxLigne4){hyp2=false;}
	if(distHyp2[coeffTrie[7]]>distMaxLigne4){hyp2=false;}
	if(distHyp2[coeffTrie[8]]>distMaxLigne4){hyp2=false;}
	if(distHyp2[coeffTrie[9]]>distMaxLigne4){hyp2=false;}
	
	if(distHyp3[coeffTrie[0]]>distMaxLigne0){hyp3=false;}
	if(distHyp3[coeffTrie[1]]>distMaxLigne0){hyp3=false;}
	if(distHyp3[coeffTrie[2]]>distMaxLigne3){hyp3=false;}
	if(distHyp3[coeffTrie[3]]>distMaxLigne3){hyp3=false;}
	if(distHyp3[coeffTrie[4]]>distMaxLigne3){hyp3=false;}
	if(distHyp3[coeffTrie[5]]>distMaxLigne3){hyp3=false;}
	if(distHyp3[coeffTrie[6]]>distMaxLigne4){hyp3=false;}
	if(distHyp3[coeffTrie[7]]>distMaxLigne4){hyp3=false;}
	if(distHyp3[coeffTrie[8]]>distMaxLigne4){hyp3=false;}
	if(distHyp3[coeffTrie[9]]>distMaxLigne4){hyp3=false;}

	if(distHyp4[coeffTrie[0]]>distMaxLigne0){hyp4=false;}
	if(distHyp4[coeffTrie[1]]>distMaxLigne0){hyp4=false;}
	if(distHyp4[coeffTrie[2]]>distMaxLigne3){hyp4=false;}
	if(distHyp4[coeffTrie[3]]>distMaxLigne3){hyp4=false;}
	if(distHyp4[coeffTrie[4]]>distMaxLigne3){hyp4=false;}
	if(distHyp4[coeffTrie[5]]>distMaxLigne3){hyp4=false;}
	if(distHyp4[coeffTrie[6]]>distMaxLigne4){hyp4=false;}
	if(distHyp4[coeffTrie[7]]>distMaxLigne4){hyp4=false;}
	if(distHyp4[coeffTrie[8]]>distMaxLigne4){hyp4=false;}
	if(distHyp4[coeffTrie[9]]>distMaxLigne4){hyp4=false;}
	

	var distanceRetenue;
	if(hyp4==true){distanceRetenue=distHyp4;}
	else{
		if (hyp3==true){distanceRetenue=distHyp3;}
		else{
			if (hyp2==true){distanceRetenue=distHyp2;}
			else{
				if (hyp1==true){distanceRetenue=distHyp1;}
				else{distanceRetenue=distHyp0;}
			}
		}
	}
	
	numeroLigne[coeffTrie[0]]=0; rajoutAngle[coeffTrie[0]]=0;placeSurLaLigne[coeffTrie[0]]=distanceRetenue[coeffTrie[0]]/coeffEmToPx;
	numeroLigne[coeffTrie[1]]=0; rajoutAngle[coeffTrie[1]]=1;placeSurLaLigne[coeffTrie[1]]=distanceRetenue[coeffTrie[1]]/coeffEmToPx;
	
	for(var i =6; i<10;i++){
		if(distanceRetenue[coeffTrie[i]]>=dist4EnPx && distanceRetenue[coeffTrie[i]]<=distMaxLigne4){
			numeroLigne[coeffTrie[i]]=4;
			placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*8)*(coeffEmToPx*8))/coeffEmToPx;
			}
		else{
			if(distanceRetenue[coeffTrie[i]]>=dist3EnPx && distanceRetenue[coeffTrie[i]]<=distMaxLigne3){
				numeroLigne[coeffTrie[i]]=3;
				placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*6)*(coeffEmToPx*6))/coeffEmToPx;
			}
			else{
				numeroLigne[coeffTrie[i]]=2;
				placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*4)*(coeffEmToPx*4))/coeffEmToPx;
			}
		}
	}
	numeroLigne[coeffTrie[8]]=-numeroLigne[coeffTrie[8]];
	numeroLigne[coeffTrie[9]]=-numeroLigne[coeffTrie[9]];
	
	rajoutAngle[coeffTrie[6]]=0;
	rajoutAngle[coeffTrie[7]]=1;
	rajoutAngle[coeffTrie[8]]=0;
	rajoutAngle[coeffTrie[9]]=1;
	
	for(var i=2;i<6;i++){
		switch(Math.abs(numeroLigne[coeffTrie[i+4]])){
			case 2:
				numeroLigne[coeffTrie[i]]=1;
				placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*2)*(coeffEmToPx*2))/coeffEmToPx;
				break;
			case 3:
				if(distanceRetenue[coeffTrie[i]]>=dist2EnPx && distanceRetenue[coeffTrie[i]]<=distMaxLigne2){
					numeroLigne[coeffTrie[i]]=2;
					placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*4)*(coeffEmToPx*4))/coeffEmToPx;
				}
				else{
					numeroLigne[coeffTrie[i]]=3;
					placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*6)*(coeffEmToPx*6))/coeffEmToPx;
				}
				break;
			case 4:
				if(distanceRetenue[coeffTrie[i]]>=dist2EnPx && distanceRetenue[coeffTrie[i]]<=distMaxLigne2){
					numeroLigne[coeffTrie[i]]=2;
					placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*4)*(coeffEmToPx*4))/coeffEmToPx;
				}
				else{
					if(distanceRetenue[coeffTrie[i]]>=dist3EnPx && distanceRetenue[coeffTrie[i]]<=distMaxLigne3){
						numeroLigne[coeffTrie[i]]=3;
						placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*6)*(coeffEmToPx*6))/coeffEmToPx;
					}
					else{
						numeroLigne[coeffTrie[i]]=1;
						placeSurLaLigne[coeffTrie[i]]=Math.sqrt(distanceRetenue[coeffTrie[i]]*distanceRetenue[coeffTrie[i]]-(coeffEmToPx*2)*(coeffEmToPx*2))/coeffEmToPx;
					}
				}
				break;
		}
	}
	rajoutAngle[coeffTrie[2]]=0;
	rajoutAngle[coeffTrie[3]]=1;
	numeroLigne[coeffTrie[4]]=-numeroLigne[coeffTrie[4]]; rajoutAngle[coeffTrie[4]]=0;
	numeroLigne[coeffTrie[5]]=-numeroLigne[coeffTrie[5]]; rajoutAngle[coeffTrie[5]]=1;

}

function sign(x) { if (x>=0){return 1} else{return -1}}

function maxTab(tableau){
	var max=0;
	for (var i=0;i<tableau.length;i++){
		if(tableau[i].value>max){
			max=tableau[i].value;
		}
	}
	return max;
}

function minTab(tableau){
	var min=-1;
	for (var i=0;i<tableau.length;i++){
		if(tableau[i].value<min || min==-1){
			min=tableau[i].value;
		}
	}
	return min;
}

function montrerResultats(nomDuCadre,data){
	//alert("hello2")
	var nbrResultats=data.results.length;
	var Afficher=new Array;
	var nomFilm=new Array;
	for (var i = nbrResultats;i<10;i++){
		Afficher[i]=false;
		coeffDist[i]=1;
		nomFilm[i]="Inexistant";
	}
	for (var i = 0;i<nbrResultats;i++){
		Afficher[i]=true;
		if(minTab(data.results)!=-1 && (maxTab(data.results)-minTab(data.results))>0){
			coeffDist[i]=(data.results[i].value-minTab(data.results))/(maxTab(data.results)-minTab(data.results))
		}
		else{
			if(maxTab(data.results)>1){
				coeffDist[i]=data.results[i].value/maxTab(data.results);
			}
			else{
				coeffDist[i]=data.results[i].value;
			}
		}
		nomFilm[i]=data.results[i].title; // CHANGER 0 par i
	}
	//alert(coeffDist)
	var cadreInter1 = document.createElement('div');
	cadreInter1.id="cadreInter1";
	cadreInter1.style.cssText ='width:100%;height:18em;top:0em;position:absolute;'//border: 1px solid Black;'
	document.getElementById(nomDuCadre).appendChild(cadreInter1);

	var carreCentral = document.createElement('div');
	carreCentral.id="carreCentral";

	var largeurBox=$("#cadreInter1").width();
	var hauteurBox=$("#cadreInter1").height();
	var coeffEmToPx=hauteurBox/18;

	longueurEtAngle(coeffDist,largeurBox,hauteurBox,coeffEmToPx);

	//carreCentral.style.cssText ='border-radius:0.5em;display: table; position:absolute;width: 6em;height: 6em;background-color: #5697DB;border: 1px solid Black;z-index:10; text-align : center ;';//white-space:nowrap;overflow:hidden;text-overflow:ellipsis;';//display: table;';
	document.getElementById("cadreInter1").appendChild(carreCentral);
	var largeurCarre=$("#carreCentral").width();
	var hauteurCarre=$("#carreCentral").height();

	carreCentral.style.left=largeurBox/2-largeurCarre/2+"px";
	carreCentral.style.top=hauteurBox/2-hauteurCarre/2+"px";

	var conteneurTexteCentral=document.createElement('p');

	conteneurTexteCentral.id="conteneurTexteCentral";
	//conteneurTexteCentral.style.cssText='display:table-cell; text-align: center;vertical-align: middle;';//text-overflow:ellipsis;overflow:hidden; white-space:nowrap;'//vertical-align: middle;'

	var contenu=document.createTextNode("");
	contenu.id="nomFilmChoisi";

	var text;
	for (var i = 0; i < document.getElementsByClassName("div hilight")[0].childNodes.length; ++i){
		if (document.getElementsByClassName("div hilight")[0].childNodes[i].nodeType === 3){
			text = document.getElementsByClassName("div hilight")[0].childNodes[i].textContent;
		}
	}	
	
	contenu.textContent=text
	document.getElementById("carreCentral").appendChild(conteneurTexteCentral);
	document.getElementById("conteneurTexteCentral").appendChild(contenu);

	var barre=new Array;
	var cadre=new Array;
	var lBarre=new Array;
	var angleBarre=new Array;
	for(var i=0;i<10;i++){
		lBarre[i]=Math.sqrt((Math.abs(numeroLigne[i])*2)*(Math.abs(numeroLigne[i])*2)+placeSurLaLigne[i]*placeSurLaLigne[i]);
		angleBarre[i]=rajoutAngle[i]*Math.PI+Math.asin(sign(numeroLigne[i])*(Math.abs(numeroLigne[i])*2)/lBarre[i]);
	}
	
	var conteneur=new Array;
	var contenuTitre=new Array;
	for (var i=0;i<10;i++){

		barre[i] = document.createElement('div');
		barre[i].id="barre"+i;
		barre[i].setAttribute('class', 'barre_lien');

		barre[i].style.cssText ='width: '+lBarre[i]+'em;left :'+(largeurBox/2-coeffEmToPx*lBarre[i]/2)+'px;top:'+(hauteurBox/2-1)+'px;transform:rotate('+angleBarre[i]+'rad) translate('+(lBarre[i]/2)+'em);-webkit-transform:rotate('+angleBarre[i]+'rad) translate('+(lBarre[i]/2)+'em)';

		document.getElementById(nomDuCadre).appendChild(barre[i]);

		cadre[i] = document.createElement('div');
		cadre[i].id="cadre"+i;
		cadre[i].setAttribute('class', 'cadre_film');
		cadre[i].style.cssText ='width: '+coeffTailleCadreTitre*largeurBox+'px;left :'+(largeurBox/2+coeffEmToPx*lBarre[i]*Math.cos(angleBarre[i]))+'px;top:'+(hauteurBox/2+coeffEmToPx*lBarre[i]*Math.sin(angleBarre[i]))+'px;transform:translate('+(-coeffTailleCadreTitre*largeurBox/2)+'px,-0.8em);-webkit-transform:translate('+(-coeffTailleCadreTitre*largeurBox/2)+'px,-0.8em)';

		document.getElementById(nomDuCadre).appendChild(cadre[i]);
		
		conteneur[i]=document.createElement('p');

		conteneur[i].id="conteneur"+i;
		conteneur[i].setAttribute('class', 'conteneur');
		//conteneur[i].style.cssText='position:relative;text-align: center;text-overflow:ellipsis;overflow:hidden; white-space:nowrap;transform:translate(0px,-0.8em);-webkit-transform:translate(0px,-0.8em)'
		//display:table-cell; text-align: center;vertical-align: middle;'

		contenuTitre[i]=document.createTextNode(nomFilm[i]);
		contenuTitre[i].id="contenuTitre"+i;
		
		document.getElementById("cadre"+i).appendChild(conteneur[i]);
		document.getElementById("conteneur"+i).appendChild(contenuTitre[i]);
		
	}

	var vitesse=2.5;
	if(Afficher[0]==true){
	setTimeout(function(){$("#barre0").fadeIn(1000/vitesse);$("#cadre0").fadeIn(1000/vitesse);},(9-0)*300/vitesse)}
	if(Afficher[1]==true){
	setTimeout(function(){$("#barre1").fadeIn(1000/vitesse);$("#cadre1").fadeIn(1000/vitesse);},(9-1)*300/vitesse)}
	if(Afficher[2]==true){
	setTimeout(function(){$("#barre2").fadeIn(1000/vitesse);$("#cadre2").fadeIn(1000/vitesse);},(9-2)*300/vitesse)}
	if(Afficher[3]==true){
	setTimeout(function(){$("#barre3").fadeIn(1000/vitesse);$("#cadre3").fadeIn(1000/vitesse);},(9-3)*300/vitesse)}
	if(Afficher[4]==true){
	setTimeout(function(){$("#barre4").fadeIn(1000/vitesse);$("#cadre4").fadeIn(1000/vitesse);},(9-4)*300/vitesse)}
	if(Afficher[5]==true){
	setTimeout(function(){$("#barre5").fadeIn(1000/vitesse);$("#cadre5").fadeIn(1000/vitesse);},(9-5)*300/vitesse)}
	if(Afficher[6]==true){
	setTimeout(function(){$("#barre6").fadeIn(1000/vitesse);$("#cadre6").fadeIn(1000/vitesse);},(9-6)*300/vitesse)}
	if(Afficher[7]==true){
	setTimeout(function(){$("#barre7").fadeIn(1000/vitesse);$("#cadre7").fadeIn(1000/vitesse);},(9-7)*300/vitesse)}
	if(Afficher[8]==true){
	setTimeout(function(){$("#barre8").fadeIn(1000/vitesse);$("#cadre8").fadeIn(1000/vitesse);},(9-8)*300/vitesse)}
	if(Afficher[9]==true){
	setTimeout(function(){$("#barre9").fadeIn(1000/vitesse);$("#cadre9").fadeIn(1000/vitesse);},(9-9)*300/vitesse)}

	$(window).resize(function() {
		largeurBox=$("#cadreInter1").width();
		hauteurBox=$("#cadreInter1").height();
		coeffEmToPx=hauteurBox/18;
		
		longueurEtAngle(coeffDist,largeurBox,hauteurBox,coeffEmToPx);

		largeurCarre=$("#carreCentral").width();
		hauteurCarre=$("#carreCentral").height();

		carreCentral.style.left=largeurBox/2-largeurCarre/2+"px";
		carreCentral.style.top=hauteurBox/2-hauteurCarre/2+"px";

		for(var i=0;i<10;i++){
			lBarre[i]=Math.sqrt((Math.abs(numeroLigne[i])*2)*(Math.abs(numeroLigne[i])*2)+placeSurLaLigne[i]*placeSurLaLigne[i]);
			angleBarre[i]=rajoutAngle[i]*Math.PI+Math.asin(sign(numeroLigne[i])*(Math.abs(numeroLigne[i])*2)/lBarre[i]);
		}		
		
		for (var i=0;i<10;i++){
			document.getElementById("barre"+i).style.width =lBarre[i]+'em';
			document.getElementById("barre"+i).style.left =(largeurBox/2-coeffEmToPx*lBarre[i]/2)+'px';
			document.getElementById("barre"+i).style.top=(hauteurBox/2-1)+'px';
			document.getElementById("barre"+i).style.transform='rotate('+angleBarre[i]+'rad) translate('+(lBarre[i]/2)+'em)';
			document.getElementById("barre"+i).style.webkitTransform='rotate('+angleBarre[i]+'rad) translate('+(lBarre[i]/2)+'em)';
			document.getElementById("cadre"+i).style.left =(largeurBox/2+coeffEmToPx*lBarre[i]*Math.cos(angleBarre[i]))+'px';
			document.getElementById("cadre"+i).style.top=(hauteurBox/2+coeffEmToPx*lBarre[i]*Math.sin(angleBarre[i]))+'px';
			document.getElementById("cadre"+i).style.width =coeffTailleCadreTitre*largeurBox+'px';
			document.getElementById("cadre"+i).style.transform='translate('+(-coeffTailleCadreTitre*largeurBox/2)+'px,-0.8em)';
			document.getElementById("cadre"+i).style.webkitTransform='translate('+(-coeffTailleCadreTitre*largeurBox/2)+'px,-0.8em)';
		}
	});

	$("#carreCentral").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 6");$("#canv6").click();}})
	$("#cadre0").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 1");$("#canv7").click();}})
	$("#cadre1").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 2");$("#canv5").click();}})
	$("#cadre2").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 3");$("#canv8").click();}})
	$("#cadre3").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 4");$("#canv4").click();}})
	$("#cadre4").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 5");$("#canv9").click();}})
	$("#cadre5").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 7");$("#canv3").click();}})
	$("#cadre6").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 8");$("#canv10").click();}})
	$("#cadre7").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 9");$("#canv2").click();}})
	$("#cadre8").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 10");$("#canv11").click();}})
	$("#cadre9").click(function(){if(carrouselDispo==true){chargementBulleInfo("cadreInfo","Film 11");$("#canv1").click();}})

}
/*$(document).ready(function(){
	montrerResultats("test");
});*/