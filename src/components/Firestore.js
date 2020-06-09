let firebase_obj = require('../FirebaseConfig');


function union_arrays (x, y) {
    var obj = {};
    for (let i = x.length-1; i >= 0; -- i)
        obj[x[i]] = x[i];
    for (let i = y.length-1; i >= 0; -- i)
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
        this.storage = firebase_obj.storage;
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
        console.log('Printing files ref');
        await this.get_phrase_csvs(query);
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

    async get_phrase_csvs(phrase){
        let path_ref = this.storage.ref(`phrase_csv/${phrase}`);
        //console.log(`PATH_REF: ${path_ref}`)

        console.log(path_ref);

        let links = await path_ref.listAll();

        //console.log(links.items);
        let promises = [];

        links.items.forEach(itemRef => {
            promises.push(itemRef.getDownloadURL());
        });
        let all_links = await Promise.all(promises);
        console.log(all_links)
        return all_links;

        /*await path_ref.listAll().then(function(res) {
            console.log("REFERECNES GOTTEN");
            res.prefixes.forEach(function(folderRef) {
                // All the prefixes under listRef.
            });
            res.items.forEach(function(itemRef) {
                // All the items under listRef.
                console.log(`ItemRef ${itemRef}`);
                // Invoke function to download all files

            });

            return res.items;




        }).catch(function(error) {
            // Uh-oh, an error occurred!
            console.log(`Error when trying to fetch from path phrase_csv/${phrase}`);
            return [];
        });*/
    }


}


module.exports = {
    'firestore': new Firestore(),
}


