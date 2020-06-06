let firebase_obj = require('../FirebaseConfig');


function union_arrays (x, y) {
    var obj = {};
    for (var i = x.length-1; i >= 0; -- i)
        obj[x[i]] = x[i];
    for (var i = y.length-1; i >= 0; -- i)
        obj[y[i]] = y[i];
    var res = []
    for (var k in obj) {
        if (obj.hasOwnProperty(k))  // <-- optional
            res.push(obj[k]);
    }
    return res;
}


class Firestore {
    constructor(){
        this.database = firebase_obj.database;
    }

    async create_query_doc(query){
        let ref = await this.database.collection('research_topics').doc(query);

        let orig_ref = ref;

        let obj = {}
        await ref.get().then(doc => {
            if (!doc.exists) {
                console.log('No such document!');
                obj =  {
                    "reports":[],
                    "term": query,
                    "twitter_data":[],
                }
                ref.set(obj,{'merge':true});
            } else {
                console.log('Document data:', doc.data());
                obj = doc.data();
            }
        })


        console.log(obj)

        let merged_reports =union_arrays(obj.reports,["Rafaeee"]);
        let merged_twitter_data = union_arrays(obj.twitter_data,["Yolo"]);


        let writeResult = await ref.update({
            "reports": merged_reports,
            "term":query,
            "twitter_data":merged_twitter_data,
        });

        console.log("Updated field with value")

        console.log(orig_ref)
        return orig_ref;
    }

    async add_query_pdf(pdf_file,label,query){
        let ref = await this.database.collection('research_topics').doc(query);


        await ref.get().then(doc => {
            let obj = doc.data();

            let merged_reports = union_arrays(obj.reports,[label]);

            ref.update({
                'reports':merged_reports,
            })
        })


    }
}


module.exports = {
    'firestore': new Firestore(),
}


