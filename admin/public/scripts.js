function mostrar_categoria(){
    let disciplina = document.getElementById("disciplina").value
    if(disciplina != "sin_cat"){
        document.getElementById(disciplina).removeAttribute('hidden')
        document.getElementById(disciplina).setAttribute('required', 'true')
        document.getElementById(disciplina).getElementsByClassName("select-input")[0].setAttribute('name', 'categoria')
    }
    let opciones = document.getElementById("disciplina").options.length; 
    for(let i=1; i<opciones; i++){
        esconder_disciplina = document.getElementById("disciplina").options[i].text;
        if(esconder_disciplina == disciplina){
            continue
        }else{
            document.getElementById(esconder_disciplina).setAttribute('hidden', 'true')
            document.getElementById(esconder_disciplina).removeAttribute('required')
            document.getElementById(esconder_disciplina).getElementsByClassName("select-input")[0].removeAttribute('name')
        }
    }
}