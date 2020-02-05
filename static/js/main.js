class CalcController {

    constructor() {
        this._locale = 'pt-BR';
        this._dateEl = document.querySelector("#data");
        this._timeEl = document.querySelector("#hora");
        this._currentDate;
        this.initialize();
    }

    initialize() {

            this.setDisplayDateTime();

            setInterval(() => {

                this.setDisplayDateTime();

            }, 1000);

        }
        //metodo para setar a data e hora no display
    setDisplayDateTime() {
            this.displayDate = this.currentDate.toLocaleDateString(this._locale, {
                day: '2-digit',
                month: 'long',
                year: 'numeric'
            });
            this.displayTime = this.currentDate.toLocaleTimeString(this._locale);

        }
        //metodo pra
    get displayTime() {
        return this._timeEl.innerHTML;

    }
    set displayTime(value) {
        return this._timeEl.innerHTML = value;

    }

    get displayDate() {
        return this._dateEl.innerHTML;

    }
    set displayDate(value) {
        return this._dateEl.innerHTML = value;

    }
    get currentDate() {
        return new Date();
    }

    set currentDate(value) {
        this.currentDate = value;
    }
}