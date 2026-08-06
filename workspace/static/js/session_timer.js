
document.addEventListener(

    "DOMContentLoaded",

    function(){
    

        const timer =
            document.getElementById(
                "countdown"
            );


        if(!timer){

            return;

        }

        let remainingSeconds = parseInt(timer.dataset.timeout, 10) * 60;
        

        const timerInterval =
            setInterval(updateTimer,1000);

        function updateTimer(){

            const minutes =
                Math.floor(
                    remainingSeconds / 60
                );

            const seconds =
                remainingSeconds % 60;

            timer.textContent =
                minutes.toString().padStart(2,"0")
                +
                ":"
                +
                seconds.toString().padStart(2,"0");

            if(remainingSeconds <= 0){

                clearInterval(
                    timerInterval
                );

                window.location =
                    "/logout";

                return;

            }

            remainingSeconds--;

        }

        updateTimer();

    }

);

