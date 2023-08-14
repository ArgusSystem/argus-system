export class Tab {
    static HOME = new Tab('Home', 'home.html');
    static LIVE_FEED = new Tab('Live Feed', 'cameras.html');
    static NOTIFICATIONS = new Tab('Notifications', 'notifications.html');
    static HISTORY = new Tab('History', 'history.html');
    static PEOPLE = new Tab('People', 'people.html');
    static AREAS = new Tab('Areas', 'areas.html');
    static RESTRICTIONS = new Tab('Restrictions', 'restrictions.html');
    static STATISTICS = new Tab('Statistics', 'statistics.html');

    constructor (name, page) {
        this.name = name;
        this.page = page;
    }

    static values() {
        return Object.keys(Tab).map(attribute => Tab[attribute]);
    }
}
