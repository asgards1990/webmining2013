
$(document).ready(function(){

critereEnable = false;
	function createClick(nom) {

		if (nom=="movieinput") {
        			
			$("#movieinput").keyup(function(event){
			if(event.keyCode == 13){
			var p = this.parentNode;
			var element = this.parentNode.parentNode;
			var value = this.value
			var textNode = document.createTextNode(value)
			p.removeChild(this);

			p.appendChild(textNode);
			element.getElementsByTagName("img")[0].src="http://goo.gl/8IrUDR";

			var deleteicon = document.createElement('div');
			deleteicon.className = "deleteicon";
			deleteicon.style="cursor: pointer;"; 

			var image = document.createElement('img');
			image.style="max-height:1.4em;max-width:1.4em";
			image.src="http://goo.gl/61lXjQ";
			image.alt="Edit";

			deleteicon.appendChild(image);
			element.appendChild(deleteicon);
			
			if (critereEnable==false) {
				var tabCriteres=document.getElementById("filters").getElementsByTagName("input");
				var formGenres=document.getElementById("genres").getElementsByTagName("form")[0];
				var formBudget=document.getElementById("slider-range");
				var formReviews=document.getElementById("ex_1b");
				
			
				critereEnable=true;
			
			for (k=0; k<tabCriteres.length;k++)   {
				tabCriteres[k].disabled=false; 
				formGenres.style.display = "block";
				formBudget.style.display = "block";
				formReviews.style.display = "block";
			
				}
			
			}
	createClick(deleteicon);
			}
		});
		

	}


		else {$(".deleteicon").click(function(){
			var p = this.parentNode.getElementsByTagName("p")[0];
			text = p.textContent;
			var element = this.parentNode;
			var movieinput = document.createElement('input');
			var newP = document.createElement('p');
			element.getElementsByTagName("img")[0].src="../pesto/static/img/explore/questionmark.png";


			element.removeChild(this);
			element.removeChild(p);


			movieinput.id="movieinput";
			movieinput.type="text";
			movieinput.name="actorname"
			movieinput.value=text;
			movieinput.size="12";
			movieinput.style="text-align : left";

			newP.appendChild(movieinput);
			element.appendChild(newP);
	
		createClick("movieinput");
			});	
		}
	};
	
createClick("movieinput");	
	
	

});

function ajoutActors (actor) {

    var superior = document.getElementById("actors").getElementsByTagName("ul")[0];

    var father = document.createElement('li');
    father.className="listactor";

    
    var paragraph = document.createElement('p');
    paragraph.className="actor";
    paragraph.id = actor.imdb_id;
  

    
    var check = document.createElement('input');
    check.type="checkbox";
    check.name="actor";
    check.value="???";
    /*check.style.cssText="position: absolute; opacity: 0;";

    var environnement = document.createElement('div');
    environnement.className="icheckbox_line-red";


    var icheck = document.createElement('div');
    icheck.className="icheck_line-icon";

    var helper = document.createElement('ins');
    helper.className="iCheck-helper";*/

    var name = document.createElement('span');
    name.className="name";

    var text = actor.first_name + " " + actor.last_name;
    name.appendChild(document.createTextNode(text));
    


    paragraph.appendChild(check);
    paragraph.appendChild(name);

    
    father.appendChild(paragraph);
    superior.appendChild(father);


                $(check).each(function () {
                var self = $(this),
                label = self.next(),
                label_text = label.text();

        label.remove();
        self.iCheck({
            checkboxClass: 'icheckbox_line-red',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        });
    });


    };
    
$(document).ready(function(){
    $("#acteurs").click(function(){
      
             var ul = document.getElementById("actors").getElementsByTagName("ul")[0];
           if (ul.hasChildNodes())
           {
               while (ul.childNodes.length>=1)
               {ul.removeChild(ul.firstChild);
                }
               };


        
            
            var actor1 = new Object;
            actor1.imdb_id="1";
            actor1.first_name= "Cate";
            actor1.last_name = "Blanchett";



            
            var actor2 = new Object;
            actor2.imdb_id="2";
            actor2.first_name= "Brad";
            actor2.last_name = "Pitt";
            
            ajoutActors(actor1);
            ajoutActors(actor2);
        });
    });
                        
$(document).ready(function(){
    $("#budgets").click(function(){
      
           var ul = document.getElementById("actors").getElementsByTagName("ul")[0];
           if (ul.hasChildNodes())
           {
               while (ul.childNodes.length>=1)
               {ul.removeChild(ul.firstChild);
                }
               };

           
            
            var actor1 = new Object;
            actor1.imdb_id="1";
            actor1.first_name= "test1";
            actor1.last_name = "test1";



            
            var actor2 = new Object;
            actor2.imdb_id="2";
            actor2.first_name= "test2";
            actor2.last_name = "test2";

            var actor3 = new Object;
            actor3.imdb_id="3";
            actor3.first_name= "test3";
            actor3.last_name = "test3";
            
            ajoutActors(actor1);
            ajoutActors(actor2);
            ajoutActors(actor3);

    });
    });

                /*<li class="listactor">
                    <p class="actor">
                    <input type="checkbox" name="actor" value="actor1">
                    <span class="name">Cate Blanchett</span>
                    </p>                       
                </li>*/
	



