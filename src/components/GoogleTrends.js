
const googleTrends = require('google-trends-api');

class GoogleTrends {
    constructor() {
    }

    // TODO: Improvde sanatising
    sanatise_query(query){
        return query.toLowerCase();

    }

    async get_related_terms(query){
        query = this.sanatise_query(query);
        let current_date = new Date()

        const getDaysInMonth = (year, month) => new Date(year, month, 0).getDate()

        const addMonths = (input, months) => {
            const date = new Date(input)
            date.setDate(1)
            date.setMonth(date.getMonth() + months)
            date.setDate(Math.min(input.getDate(), getDaysInMonth(date.getFullYear(), date.getMonth()+1)))
            return date
        }



        let res = await fetch(`/google_trend/${query}`).then(res => res.json());
        //.then(data => {
        //console.log(data)
        //});
        return res;







    }
}



export default GoogleTrends;

/*
let trend_obj = new GoogleTrends();

module.exports = {
    'trend_obj':trend_obj,
}
 */