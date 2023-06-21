import { markSelected } from '../../../components/select2.js';

export function select(restrictions, element, type) {
    markSelected(element, restrictions
        .filter(restriction => restriction.type === type)
        .flatMap(restriction => restriction.value.map(v => v.toString())));
}