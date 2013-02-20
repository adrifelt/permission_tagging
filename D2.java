import com.gc.android.market.api.MarketSession;
import com.gc.android.market.api.model.Market.AppsRequest;
import com.gc.android.market.api.model.Market.AppsResponse;
import com.gc.android.market.api.model.Market.ResponseContext;
import com.gc.android.market.api.model.Market.GetAssetResponse.InstallAsset;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.io.FileReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.HashSet;

public class D2 {
    private static final int ENTRIES_COUNT = 10;

    private static final int MAX_INDEX = 800;//800;

    private static final String META_PATH = "apps/";

    @SuppressWarnings("unused")
    private static final int START_INDEX = 0;

    private static final int I_START = START_INDEX; // for rerunning

    private static final long TIMEOUT = 60000L;

    private static final long SLEEP_TIME_META = 12000L;

    private static final long SLEEP_TIME_DWNLD = 60000L;

    private static final long SLEEP_TIME_RETRY = 2000L;

    //private static final String[] categories = {
    //        "Comics", "Communication", "Entertainment", "Finance", "Health", "Lifestyle",
    //        "Multimedia", "News", "Productivity", "Reference", "Shopping", "Social", "Sports",
    //        "Themes", "Tools", "Travel", "Demo", "Libraries", "Arcade", "Brain", "Cards", "Casual"
    //};

    private static final String[] categories = {
        "BOOKS_AND_REFERENCE", "BUSINESS", "COMICS", "COMMUNICATION", "EDUCATION", "ENTERTAINMENT", "FINANCE",
        "HEALTH_AND_FITNESS", "LIBRARIES_AND_DEMO", "LIFESTYLE", "APP_WALLPAPER", "MEDIA_AND_VIDEO", "MEDICAL",
        "MUSIC_AND_AUDIO", "NEWS_AND_MAGAZINES", "PERSONALIZATION", "PHOTOGRAPHY", "PRODUCTIVITY", "SHOPPING", "SOCIAL",
        "SPORTS", "TOOLS", "TRANSPORTATION", "TRAVEL_AND_LOCAL", "WEATHER", "APP_WIDGETS", "ARCADE", "BRAIN", "CARDS",
        "CASUAL", "GAME_WALLPAPER", "RACING", "SPORTS_GAMES", "GAME_WIDGETS"
    };

    private static String cat;

    private static PrintWriter metaInfo;
    private static HashSet<String> idsDone = new HashSet<String>();

    private static final Semaphore prevReqDone = new Semaphore(0);

    private static MarketSession secureSession;

    public static void main(String[] args) {
        System.out.println("hello world");
        try {
            /*
             * if(args.length < 2) { System.out.println("Usage :\n" +
             * "market email password query"); return; }
             */

            //String login = "droid000111@gmail.com"; // args[0];
            //String password = "Droid10^"; // args[1];
            String login = "zyqu1990@gmail.com";
            String password = "62813123ABc";
            String androidid = "3bb147c21609a298";
	    /*String login = "cn2ben@gmail.com";
            String password = "zhangweiMcde2m";
            String androidid = "36f70274cc55cccf";*/
             String query = args.length > 0 ? args[0] : "lookout";
            // cat = args.length > 2 ? args[2] : "Comics";

            //BufferedReader idReader = new BufferedReader(new FileReader(META_PATH + "idsDl.txt"));
            //String id;
            //while ((id = idReader.readLine()) != null) {
            //    id = id.trim();
            //    if (id.equals("") || id.startsWith("#")) //ignore empty lines and comments
            //        continue;
            //    String[] tokens = id.split("\\s+");
            //    idsDone.add(tokens[0]);
            //}
            //idReader.close();

            //idWriter = new PrintWriter(new FileWriter(META_PATH + "idsDl.txt", true), true);

            //for (String dir : categories)
            //    (new File(META_PATH + dir)).mkdir();

            MarketSession session = new MarketSession(false);
            session.getContext().setDeviceAndSdkVersion("sapphire:7");
            System.out.println("Login...");
            session.login(login, password,androidid);
            System.out.println("Login done");

            secureSession = new MarketSession(true);
            System.out.println("Login...");
            secureSession.login(login, password,androidid);
            System.out.println("Login done");

            metaInfo = new PrintWriter(new FileWriter("200appsFeb13_3meta.txt", false), true);

            //AppsRequest req = makeRequest(query);
            //processRequest(session, req);

            //for (int i = I_START; i < MAX_INDEX; i += ENTRIES_COUNT) {
            //    AppsRequest req = makeRequest(query, i, ENTRIES_COUNT);
            //    processRequest(session, req); 
            //    Thread.sleep(SLEEP_TIME_META);
            //}

            //for (int i = I_START; i < MAX_INDEX; i += ENTRIES_COUNT) {
            //    AppsRequest req = makeRequest(i, ENTRIES_COUNT);
            //    processRequest(session, req); 
            //    Thread.sleep(SLEEP_TIME_META);
            //}

            //for (int i = I_START; i < MAX_INDEX; i += ENTRIES_COUNT) {
            //    for (String catClone : categories) {
            //        cat = catClone;
            ////cat = categories[13];
            //        System.out.println("At iteration i = " + i + ", category = " + cat);
            //        //if (cat.equalsIgnoreCase("comics"))
            //            //processRequest(session, 192, 8);
            //        //else
            //            processRequest(session, i, ENTRIES_COUNT);
            //        Thread.sleep(SLEEP_TIME_META);
            //    }
            //}
	    //cat = "HEALTH_AND_FITNESS";
            for (int i = I_START; i < MAX_INDEX; i += ENTRIES_COUNT) {
                    //System.out.println("At iteration i = " + i + ", category = " + cat);
			//AppsRequest req = makeRequestCat(cat, i, ENTRIES_COUNT);
		if (i>401 && i<603){
			AppsRequest req = makeRequest(query, i, ENTRIES_COUNT);
			processRequest(session, req);
                    Thread.sleep(SLEEP_TIME_META);
		}
            }
            /*
             * session.append(imgReq, new Callback<GetImageResponse>() {
             * @Override public void onResult(ResponseContext context,
             * GetImageResponse response) { try { FileOutputStream fos = new
             * FileOutputStream("icon.png");
             * fos.write(response.getImageData().toByteArray()); fos.close(); }
             * catch(Exception ex) { ex.printStackTrace(); } } });
             * session.flush(); session.append(commentsRequest, callback);
             * session.flush();
             */
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private static AppsRequest makeRequest(String query, int startIndex, int count) {
        return AppsRequest.newBuilder()
            .setQuery(query)
            .setViewType(AppsRequest.ViewType.FREE)
            .setStartIndex(startIndex)
            .setEntriesCount(count)
            .setWithExtendedInfo(true)
            .build();
    }

    private static AppsRequest makeRequest(int startIndex, int count) {
        return AppsRequest.newBuilder()
                .setOrderType(AppsRequest.OrderType.POPULAR)
                .setViewType(AppsRequest.ViewType.FREE)
                .setWithExtendedInfo(true)
                .setStartIndex(startIndex).setEntriesCount(count).build();
    }

    private static AppsRequest makeRequestCat(String cat, int startIndex, int count) {
        return AppsRequest.newBuilder()
		.setCategoryId(cat)
                .setOrderType(AppsRequest.OrderType.POPULAR)
                .setViewType(AppsRequest.ViewType.FREE)
                .setWithExtendedInfo(true)
                .setStartIndex(startIndex).setEntriesCount(count).build();
    }

    private static void processRequest(MarketSession session, AppsRequest appsRequest) {

        /*
         * CommentsRequest commentsRequest = CommentsRequest.newBuilder()
         * .setAppId("7065399193137006744") .setStartIndex(0)
         * .setEntriesCount(10) .build(); // GetImageRequest imgReq =
         * GetImageRequest.newBuilder().setAppId("-7934792861962808905" )
         * .setImageUsage(AppImageUsage.SCREENSHOT) .setImageId("1") .build();
         */

        MarketSession.Callback<AppsResponse> callback = new MarketSession.Callback<AppsResponse>() {

            @Override
            public void onResult(ResponseContext context, AppsResponse response) {
                try {
                    System.out.println(response);
                    metaInfo.println(response);
                    for (int j = 0; j < response.getAppCount(); j++) {
                        // note: we have our own synchrnoization so
                        // a static cat works
                        String id = response.getApp(j).getId();
                        String pname = response.getApp(j).getPackageName();
                        //System.out.println(id);
                        //System.out.println(response.getApp(j).getPackageName());
                        Thread.sleep(SLEEP_TIME_DWNLD);
                        download(id, pname);
                    }
                } catch (Exception ex) {
                    System.out.println("exception downloading");
                    ex.printStackTrace();
                }
                try {
                    //FileWriter fstream = new FileWriter(META_PATH + cat + "/out.txt", true);
                    //BufferedWriter fout = new BufferedWriter(fstream);
                    //fout.write("Response : " + response);
                    //fout.close();
                } catch (Exception ex) {
                    System.out.println("exception writing metadata");
                    ex.printStackTrace();
                }
                prevReqDone.release();
            }

        };
        try {
            session.append(appsRequest, callback);
            session.flush();
            if (!prevReqDone.tryAcquire(TIMEOUT, TimeUnit.MILLISECONDS))
                System.out.println("waiting time elapsed; will not retry this set");
        } catch (RuntimeException ex) {
            if (ex.toString().contains("Response code = 400")) {
                //if (count > 1) {
                //    try {
                //        Thread.sleep(SLEEP_TIME_RETRY);
                //    } catch (InterruptedException e) {
                //        e.printStackTrace();
                //    }
                //    System.out.println("received 400 response code... At i = " + i
                //            + ", retrying with count " + (count - 1));
                //    //processRequest(session, i + 1, count - 1);
                //} else
                //    System.out.println("received 400 response code... giving up");
            } else {
                ex.printStackTrace();
                System.exit(1);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public static void download(String assetId, String pname) {
        String fname = "200appsFeb13_3/" + pname + ".apk";

        try {
            InstallAsset ia = secureSession.queryGetAssetRequest(assetId).getInstallAsset(0);
            String cookieName = ia.getDownloadAuthCookieName();
            String cookieValue = ia.getDownloadAuthCookieValue();

            URL url = new URL(ia.getBlobUrl());
            HttpURLConnection conn = (HttpURLConnection)url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("User-Agent", "Android-Market/2 (sapphire PLAT-RC33); gzip");
            conn.setRequestProperty("Cookie", cookieName + "=" + cookieValue);

            InputStream inputstream =  (InputStream) conn.getInputStream();
            BufferedOutputStream stream = new BufferedOutputStream(new FileOutputStream(fname));
            byte buf[] = new byte[1024];
            int k = 0;
            for(long l = 0L; (k = inputstream.read(buf)) != -1; l += k )
                stream.write(buf, 0, k);
            inputstream.close();
            stream.close();

            System.out.println("File " + fname + " saved...");
        } catch (FileNotFoundException e) {
            System.err.println("Bad url address!");
        } catch (UnsupportedEncodingException e) {
            System.out.println(e);
        } catch (MalformedURLException e) {
            System.out.println(e);
        } catch (IOException e) {
            if (e.toString().contains("HTTP response code: 403"))
                System.err.println("Forbidden response received!");
            System.out.println(e);
        }
    }
}
