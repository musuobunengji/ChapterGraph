import { ActionTypes } from "./types.js";

function reducer(currentState, action) {
    switch (action.type) {
        case ActionTypes.LOAD_GRAPH_START: {
            return { uiPhase: "loading" };
        }
        case ActionTypes.LOAD_GRAPH_SUCCESS: {
            return {
                graph: action.payload.graph,
                expandedBooks: new Set(),
                uiPhase: "ready",
            };
        }
        case ActionTypes.TOGGLE_BOOK: {
            const bookId = action.payload.bookId;
            const nextExpanded = new Set(currentState.expandedBooks);
            if (nextExpanded.has(bookId)) {
                nextExpanded.delete(bookId);
            } else {
                nextExpanded.add(bookId);
            }
            return { expandedBooks: nextExpanded };
        }
        case ActionTypes.SET_HOVERED_NODE: {
            return { hoveredNode: action.payload.node };
        }
        case ActionTypes.SET_TRANSFORM: {
            return { transform: action.payload.transform };
        }
        case ActionTypes.SET_THEME: {
            return { theme: action.payload.theme };
        }
        case ActionTypes.RESIZE: {
            return { dimensions: action.payload.dimensions };
        }
        default:
            console.warn("Unknown action", action);
            return {};
    }
}

export { reducer };
