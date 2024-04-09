class Cell {
    constructor(id) {
        this.id = id;
        this.audio = null;
        this.enabled = false;
    }


    addAudio(audio) {
        this.audio = audio;
    }

    setEnable(value) {
        this.enabled = value;
    }

    isEnabled() {
        return this.enabled;
    }

    hasAudio() {
        return this.audio !== null;
    }

    getAudio() {
        return this.audio;
    }

    getId() {
        return this.id;
    }
}

export {Cell};