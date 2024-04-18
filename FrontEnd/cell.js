class Cell {
    constructor(id) {
        this.id = id;
        this.audio = null;
    }

    addAudio(audio) {
        this.audio = audio;
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