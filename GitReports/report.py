from datetime import datetime
from typing import List

import pandas as pd
from github.PullRequest import PullRequest
from github.Repository import Repository

from . import mappings


class ReportBuilder:
    def __init__(self, repo: Repository):
        self._repo = repo

    @property
    def subject(self):
        return f"GitReports Weekly Update - {self._repo.name}"

    def build(self, cutoff: datetime = None) -> str:
        pulls = self._repo.get_pulls()

        return f"""
        <html lang="en" data-color-mode="auto" data-light-theme="light" data-dark-theme="dark">
            {self._head()}
            <body class="logged-out env-production page-responsive intent-mouse" style="word-wrap: break-word;">
                <div class="application-main " data-commit-hovercards-enabled="" data-discussion-hovercards-enabled=""
                    data-issue-and-pr-hovercards-enabled="">
                    <div itemscope="" itemtype="http://schema.org/SoftwareSourceCode" class="">
                        <main id="js-repo-pjax-container" data-pjax-container="">
                            <header role="banner">
                                <div class="d-flex flex-wrap flex-items-center pt-3 hide-full-screen mb-2">
                                <table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="842195fd-deee-40f2-9dc0-42c64a5b28d1">
                                    <tbody>
                                    <tr>
                                        <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
                                        <a class=" Header-link align-center" href="https://github.com/" data-hotkey="g d" aria-label="Homepage ">
                                            <svg  height="52" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="52" data-view-component="true" class="octicon octicon-mark-github v-align-middle">
                                                <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                                            </svg>
                                        </a>
                                    </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                            </header>
                            {self._intro()}
                                <div class="clearfix new-discussion-timeline container-xl px-3 px-md-4 px-lg-5">
                                    <div id="repo-content-pjax-container" class="repository-content ">
                                        <div class="js-check-all-container" data-pjax="">
                                            <div class="Box mt-3 Box--responsive hx_Box--firstRowRounded0">
                                                <div class="Box-header d-flex flex-justify-between" id="js-issues-toolbar"
                                                    data-pjax="#repo-content-pjax-container">
                                                    <div class="table-list-filters flex-auto d-flex min-width-0">
                                                        <div class="flex-auto d-none d-lg-block no-wrap">
                                                            Pull Requests
                                                        </div>
                                                    </div>
                                                </div>
                                                <div data-issue-and-pr-hovercards-enabled="">
                                                    <div class="js-navigation-container js-active-navigation-container">
                                                        <div class = "mb-3">
                                                            {self._pr_table(pulls,cutoff)}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {self._unsubscribe()}
                        </main>
                    </div>
                </div>
            </body>
        </html>
        """

    def _pr_table(self,
                  pulls: List[PullRequest],
                  cutoff: datetime = None) -> str:
        pr_df = pd.json_normalize(map(lambda pr: pr._rawData, pulls), sep='_')
        pr_df['created_at'] = pr_df['created_at'].apply(
            lambda dt: datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ'))
        if cutoff:
            pr_df = pr_df[pr_df.created_at > cutoff]

        target_mappings = {
            'state': mappings.state,
            'created_at': mappings.str_time,
            'title': mappings.identic,
            'user_login': mappings.identic,
        }
        return pr_df[target_mappings.keys()].to_html(
            index=False,
            justify='inherit',
            formatters=target_mappings,
            escape=False,
            border=.5,
            classes='px-3')

    def _head(self) -> str:
        """
        Raw HTML for stylesheets. Would redo with time, but outside the scope of this project
        so we're just going to use Github's existing stylesheets
        """
        return """
            <head>
                <meta charset="utf-8">
                <link rel="dns-prefetch" href="https://github.githubassets.com">
                <link rel="dns-prefetch" href="https://avatars.githubusercontent.com">
                <link rel="dns-prefetch" href="https://github-cloud.s3.amazonaws.com">
                <link rel="dns-prefetch" href="https://user-images.githubusercontent.com/">
                <link rel="preconnect" href="https://github.githubassets.com" crossorigin="">
                <link rel="preconnect" href="https://avatars.githubusercontent.com">
                <link crossorigin="anonymous" media="all"
                    integrity="sha512-1G4rYJktwRTQKn7fVfJUxH8RRZFUJlGo77xMZfBfIhZPx4BHVrzPE1VgnafttXI8G3y/PywH3uXyhNkSLp3+oA=="
                    rel="stylesheet" href="https://github.githubassets.com/assets/light-d46e2b60992dc114d02a7edf55f254c4.css">
                <link crossorigin="anonymous" media="all"
                    integrity="sha512-hI5b2oqTE9njfjYrfuzXqA4bSGSNrE5OMc9IiFhZy+RDGg9Qn4Si1A97o0MlinlwFt3xAifvoLX0s7jHmHSvVw=="
                    rel="stylesheet" href="https://github.githubassets.com/assets/dark-848e5bda8a9313d9e37e362b7eecd7a8.css">
                <link data-color-theme="dark_dimmed" crossorigin="anonymous" media="all"
                    integrity="sha512-klQdb3t14AYaRMkB0v9buaf5Ftfbec/sbxdkvyQpG6oBvzZxxH6N5QwA4llOyZsoyjqiZaTra2ci5TgInnLqQg=="
                    rel="stylesheet"
                    data-href="https://github.githubassets.com/assets/dark_dimmed-92541d6f7b75e0061a44c901d2ff5bb9.css">
                <link data-color-theme="dark_high_contrast" crossorigin="anonymous" media="all"
                    integrity="sha512-CBsfpBvg1D/Hvn8FFY4JwUVgoKjgynOSFKwgThDHrHASVid/Isgz0ueab5xSuSVx8vEvNL9UfYcpWIJRJYTCjg=="
                    rel="stylesheet"
                    data-href="https://github.githubassets.com/assets/dark_high_contrast-081b1fa41be0d43fc7be7f05158e09c1.css">
                <link data-color-theme="dark_colorblind" crossorigin="anonymous" media="all"
                    integrity="sha512-09ipkynAtzCqasl2D2//N51bUOVnOzBFdadcXdMWyphI81s1FWmJ9AD1NRq3e0PMfiJEiVSm9mjTYd7gv2xtWA=="
                    rel="stylesheet"
                    data-href="https://github.githubassets.com/assets/dark_colorblind-d3d8a99329c0b730aa6ac9760f6fff37.css">
                <link data-color-theme="light_colorblind" crossorigin="anonymous" media="all"
                    integrity="sha512-OJwnC/pGdOV3QMoWud8vp0nxtQhtzAcpNWB7mSSh/e7fPslExSb07EOdNTAJsBAS4bN7Yrdxm2F7htANgTIMsA=="
                    rel="stylesheet"
                    data-href="https://github.githubassets.com/assets/light_colorblind-389c270bfa4674e57740ca16b9df2fa7.css">
                <link crossorigin="anonymous" media="all"
                    integrity="sha512-T3N453hWCYsL8yKfu3yye2yyO/D51Lq2iT5svAdl7UKvV2rBPcV7iOgr3fihzB9vYV7YFIK3PxpyTTkfxAshog=="
                    rel="stylesheet" href="https://github.githubassets.com/assets/frameworks-4f7378e77856098b0bf3229fbb7cb27b.css">
                <link crossorigin="anonymous" media="all"
                    integrity="sha512-86nXK7G/1oWlRy1vPOOQk1LE0Bom64aEW+v5THHCA+8mxZ3bLwUUh5fUND/8b8hkArmzVw9ga1PQVgrjt75bzg=="
                    rel="stylesheet" href="https://github.githubassets.com/assets/behaviors-f3a9d72bb1bfd685a5472d6f3ce39093.css">
                <link crossorigin="anonymous" media="all"
                    integrity="sha512-MCJFYfbQoT4EXC6aWx5Wghs8FC/jslHEeN2iWXphliccmede2dQlhIBTAUCBq9Yu5poltu4askungzvyCsycGg=="
                    rel="stylesheet"
                    href="https://github.githubassets.com/assets/tab-size-fix-30224561f6d0a13e045c2e9a5b1e5682.css">
                <link crossorigin="anonymous" media="all"
                    integrity="sha512-qRZXNzipxvtgjvL3aOguJ2wmKSN3A9hBN2AK8UvO79Ss2UiUtAjZ2tTSQljbs4Fw9iN63kdXTuROvJEHVVsGFw=="
                    rel="stylesheet" href="https://github.githubassets.com/assets/github-a916573738a9c6fb608ef2f768e82e27.css">
            </head>
        """

    def _intro(self) -> str:
        return f"""
                <div id="repository-container-header" class="pt-3 hide-full-screen mb-5"
                    style="background-color: var(--color-page-header-bg);" data-pjax-replace="">
                    <div class="d-flex mb-3 px-3 px-md-4 px-lg-5">
                        <div class="flex-auto min-width-0 width-fit mr-3">
                            <h1 class=" d-flex flex-wrap flex-items-center wb-break-word f3 text-normal">
                                <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16"
                                    data-view-component="true" class="octicon octicon-repo color-fg-muted mr-2">
                                    <path fill-rule="evenodd"
                                        d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z">
                                    </path>
                                </svg>
                                <span class="author flex-self-stretch" itemprop="author">
                                    <a class="url fn" rel="author" data-hovercard-type="organization"
                                    href="{self._repo.owner.html_url}">{self._repo.owner.login}</a>
                                </span>
                                <span class="mx-1 flex-self-stretch color-fg-muted">/</span>
                                <strong itemprop="name" class="mr-2 flex-self-stretch">
                                    <a data-pjax="#repo-content-pjax-container"
                                        href="{self._repo.html_url}">{self._repo.name}</a>
                                </strong>
                                <span></span>
                            </h1>
                        </div>
                    </div>
                </div>
        """

    def _unsubscribe(self) -> str:
        """
        Not implemented yet.
        When api route is created to subscribe/unsubscribe from repos, this will redirect users to it
        """
        return ""
