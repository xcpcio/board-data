import {
    Rating,
    createContest,
    createTeams,
    createSubmissions,
    Rank,
} from "@xcpcio/core";
import fs from "node:fs";
import { resolve } from "node:path";

import { ratingConfig } from "./rating-config";

function main() {
    const rating = Rating.fromJSON(ratingConfig);
    fs.mkdirSync(resolve(__dirname, `../rating-data/${rating.id}`), {
        recursive: true,
    });

    for (const contestID of rating.contestIDs) {
        const contestData = fs.readFileSync(
            resolve(__dirname, `../data/${contestID}/config.json`)
        );
        const teamData = fs.readFileSync(
            resolve(__dirname, `../data/${contestID}/team.json`)
        );
        const runData = fs.readFileSync(
            resolve(__dirname, `../data/${contestID}/run.json`)
        );

        const contestJSON = JSON.parse(contestData.toString());
        const teamJSON = JSON.parse(teamData.toString());
        const runJSON = JSON.parse(runData.toString());

        const contest = createContest(contestJSON);
        const teams = createTeams(teamJSON);
        const submissions = createSubmissions(runJSON);

        const rank = new Rank(contest, teams, submissions);
        rank.contest.id = contestID;

        rating.ranks.push(rank);

        console.log(`Read Data Successfully. [contestID=${contestID}]`);
    }

    rating.buildRating();
    fs.writeFileSync(
        resolve(__dirname, `../rating-data/${rating.id}/rating.json`),
        JSON.stringify(rating)
    );
    console.log(`Build Rating Successfully.`);
}

main();
