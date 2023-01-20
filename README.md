<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->




<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://imgur.com/G3c0e8w.jpeg" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Ultima Discord Bot</h3>

![Python]
![Solidity]
![MySQL]

  <p align="center">
    Facilitating the organization of grassroot esport gaming communities.
    <br />
    <a href="https://github.com/dtpittman7/discord-wagers"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    · <a href="https://discord.gg/A5Y5dXNheH">Invite to Server</a>
    ·
    
  </p>
</div>




<!-- ABOUT THE PROJECT -->
## About The Project

A discord bot that allows users in a server to challenge each other to a series of a game and stores users stats as it occurs. It's the return of the dollar wager matches from GameBattles but with Smash Brothers. Ultimate. 

Here's why:
* The script mimics chess in assigning users an ELO rating, which is affected by the results of a challenge.
* These stats are displayed on the server website as well as on a smart contract where all events occured is logged onto the server as well.
* The smart contract also allows users to deposit Ethereum into their account to enable the ability to wager cryptocurrency on a challenge between users as well. 

This is definetly something still in progress, the hardest part is building a community. Will continue to iterate on this, this has been built primarily because this is something my friends and I been wanting for a long time.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Prerequisites

* A Ethereum Wallet
* Discord Account
* Profile Picture

## Slash Commands

    /initializeUser(ethereum_addy, profilepic)
    - Used to initialize yourself in the server and contract.
    /challenge(member, wager)
    - initiate a challenge with `member`. pass true if want to wager ethereum, else false. challenge will only affect win/loss total, not ELO.
    /getRank()
    - Retreives the relative rank of `member` stored on the local database.
    /getBalance(member)
    - Retreive balance of `member` stored on the smart contract.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Initiate Season 0
- [x] Rewrite to transition from prefix to slash command
- [x] Launch a website to display leaderboard
- [ ] Initiate Season 1
  - [ ] Schedule tourney date and initate open play.
- [ ] Launch on main net.
- [ ] Publicise on social media to increase member count.
- [ ] Polish confirmation sequence / deny sequence.



<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Discord: unterrorize#6321
Email: deantapittman@yahoo.com


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png

[Python]: https://img.shields.io/badge/Python-3.8-yellow
[Solidity]: https://img.shields.io/badge/Solidity-0.8.17-blue
[MySQL]: https://img.shields.io/badge/MySQL----green


[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 

