apikey = require('/var/isucon/hubot/scripts/apikey')
xml2json = require('xml2json')

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
  robot.respond /(\w+)\s+deploy/, (res) ->
    deploy robot, res, res.match[1]
  robot.respond /ベンチマーク|benchmark/, (res) ->
    benchmark robot, res
  robot.router.post '/rundeck/notify', (req, res) ->
    data = if req.body.payload? then xml2json.toJson(req.body.payload) else req.body
    trigger = data.notification.trigger
    status = data.notification.status
    execution = data.notification.executions[0]
    permalink = execution.permalink
    job_name = execution.job.name
    attachment = {
      title: "#{job_name} ##{data.notification.executionId}",
      title_link: permalink
    }
    switch trigger
      when 'start'
        attachment.pretext = "#{job_name}を始めました！"
        attachment.color = 'warning'
      when 'success'
        attachment.pretext = "八神さん、#{job_name}が終わりました！"
        attachment.color = 'good'
      when 'failure'
        attachment.pretext = "うぅ、#{job_name}に失敗しちゃった…… "
        attachment.color = 'danger'
    res.send {
      attachments: [attachment]
    }
