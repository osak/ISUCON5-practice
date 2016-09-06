apikey = require('/var/isucon/hubot/scripts/apikey')

run_job = (robot, guid, callback) ->
  robot.http("http://#{apikey.server_name}/api/14/job/#{guid}/run")
    .header('X-Rundeck-Auth-Token', apikey.auth_token)
    .header('Content-Type', 'application/json')
    .header('Accept', 'application/json')
    .post() callback

deploy = (robot, res, product) ->
  guid = apikey.product_to_guid[product.toLowerCase()]
  if guid
    run_job robot, guid, (err, _, body) ->
      if err
        res.reply "なんかうまく行きませんでした…… #{err}"
      else
        data = JSON.parse body
        msg = 'デプロイしときました！'
        if product.toLowerCase() == 'aoba'
          msg = 'な、なんか自分をデプロイするのってドキドキしますね……'
        res.reply "#{msg} #{data.permalink}"  

benchmark = (robot, res) ->
  run_job robot, apikey.benchmark_guid, (err, _, body) ->
    if err
      res.reply "失敗しちゃいました…… #{err}"
    else
      data = JSON.parse body
      res.reply "よーし、張り切ってやっちゃいますよー！ #{data.permalink}"

module.exports = (robot) ->
  robot.hear /^今日も[1１一]日$/, (res) ->
    res.send "がんばるぞい！"
  robot.respond /(\w+)\s*[をの]?デプロイ/, (res) ->
    deploy robot, res, res.match[1]
  robot.respond /deploy\s+(\w+)/, (res) ->
    deploy robot, res, res.match[1]
  robot.respond /ベンチマーク/, (res) ->
    benchmark robot, res
