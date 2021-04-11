package com.example.digitpad;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.TextView;

import com.example.digitpad.ml.DigitMl;

import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.support.label.Category;

import java.io.IOException;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private Button predictButton,clearButton ;
    private MyCanvasView myCanvasView;
    private Context context ;
    private FrameLayout frameLayout ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        context=this;

        myCanvasView = new MyCanvasView(this);
        frameLayout = (FrameLayout)findViewById(R.id.MyCanvas) ;
        frameLayout.addView(myCanvasView);

        predictButton=(Button)findViewById(R.id.Predict) ;
        clearButton=(Button)findViewById(R.id.clear) ;

        predictButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    predictModel() ;
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

        clearButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                clearCanvas() ;
            }
        });

    }

    private void predictModel() throws IOException {
        Bitmap bitmap=myCanvasView.getBitmap();
        DigitMl digitModel = DigitMl.newInstance(context) ;

        TensorImage image = TensorImage.fromBitmap(bitmap);
        DigitMl.Outputs outputs = digitModel.process(image);

        List<Category> probability = outputs.getProbabilityAsCategoryList();

        float maxScore=-1;String Digit="0" ;

        for(int i=0;i<probability.size();i++){

            Category p = probability.get(i) ;
            if( p.getScore() > maxScore ){
                maxScore=p.getScore();
                Digit=p.getLabel();
            }

        }

        digitModel.close();

        TextView textView = (TextView)findViewById(R.id.PredictedDigit) ;
        textView.setText(Digit);
    }

    private void clearCanvas(){
        frameLayout.removeAllViews();
        myCanvasView=new MyCanvasView(this) ;
        frameLayout.addView(myCanvasView);
    }


}