(function(){

    var updateClock = function(){
        var date = new Date(),
            hours = date.getHours(),
            ampm,
            minutes = date.getMinutes(),
            seconds = date.getSeconds(),
            dayWeek = date.getDay(),
            day = date.getDate(),
            month = date.getMonth(),
            year = date.getFullYear()

        var pHours = document.getElementById('hours'),
            pAMPM = document.getElementById('ampm'),
            pMinutes= document.getElementById('minutes'),
            pSeconds= document.getElementById('seconds'),
            pDayWeek= document.getElementById('dayWeek'),
            pDay = document.getElementById('day'),
            pMonth = document.getElementById('month'),
            pYear = document.getElementById('year')

        var week = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'],
        months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

        pDayWeek.textContent = week[dayWeek]
        pDay.textContent = day
        pMonth.textContent = months[month]
        pYear.textContent = year

        if(hours < 10){hours = '0' + hours};

        pHours.textContent = hours

        if(seconds < 10){seconds = '0' + seconds};

        pSeconds.textContent = seconds

        if(minutes < 10){minutes = '0' + minutes};
        pMinutes.textContent = minutes
        


    };




    updateClock();
    var intervalo = setInterval(updateClock, 1000)
}())