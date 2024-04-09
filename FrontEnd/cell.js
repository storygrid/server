class Cell {
    constructor(piece) {
        this.piece = piece;
        this.actions = []
    }

    addAction(action) {
        this.actions.push(action)
    }

    getPlainObject() {
        return {
            piece: this.piece,
            actions: this.actions
        };
    }
}

export {Cell};