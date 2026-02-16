source "https://rubygems.org"

# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec jekyll serve`,
# which uses this Gemfile.

gem "jekyll", "~> 3.9"

# This is the default theme for new Jekyll sites. You may change this to anything you like.
# gem "minima", "~> 2.5"

# If you want to use GitHub Pages, remove the "gem "jekyll"" above and
# uncomment the line below. To upgrade, run `bundle update github-pages`.
gem "github-pages", group: :jekyll_plugins

# Since you are on Ruby 2.7, pin dependencies to compatible versions:
gem "ffi", "~> 1.16.3"
gem "bigdecimal", "~> 3.1.0"
gem "drb", "~> 2.0.6"
gem "base64", "~> 0.2.0"
gem "mutex_m", "~> 0.2.0"
gem "activesupport", "< 7.1"

# If you have any plugins, put them here!
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-seo-tag"
  gem "kramdown-parser-gfm"
end

# Windows and JRuby does not support EventMachine
gem "webrick", "~> 1.7"
