import { fetchPeople } from './api/people.js';
import { createAccordion } from './people/accordion.js'

$(document).ready(async () => {
    const people = await fetchPeople();

    createAccordion(people);
});