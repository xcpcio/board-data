import {
    Rating,
    createContest,
    createTeams,
    createSubmissions,
    Rank,
} from "@xcpcio/core";
import { IRating, IRatingIndex } from "@xcpcio/types";

import fs from "node:fs";
import { resolve } from "node:path";

import { ratingConfigs } from "./rating-config";

function buildRating(ratingConfig: IRating): Rating {
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

    rating.ranks.sort((a, b) =>
        a.contest.startTime.isBefore(b.contest.startTime) ? -1 : 1
    );
    rating.buildRating();
    rating.users.sort((a, b) => b.rating - a.rating);
    fs.writeFileSync(
        resolve(__dirname, `../rating-data/${rating.id}/rating.json`),
        JSON.stringify(rating)
    );

    console.log(`Build Rating Successfully. [ratingID=${ratingConfig.id}]`);

    return rating;
}

function genIndex(ratings: Rating[]) {
    fs.mkdirSync(resolve(__dirname, `../rating-data/index`), {
        recursive: true,
    });

    const ratingIndexList: IRatingIndex[] = ratings.map((rating) => ({
        id: rating.id,
        name: rating.name,
    }));

    fs.writeFileSync(
        resolve(__dirname, `../rating-data/index/index.json`),
        JSON.stringify(ratingIndexList)
    );
}

function main() {
    fs.rmSync(resolve(__dirname, `../rating-data`), {
        recursive: true,
    });

    const ratings: Rating[] = [];
    for (const ratingConfig of ratingConfigs) {
        const rating = buildRating(ratingConfig);
        ratings.push(rating);
    }

    genIndex(ratings);
}

main();
